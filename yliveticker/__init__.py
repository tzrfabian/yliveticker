import base64
import json
from .logger import writeline
from datetime import datetime
import websocket

from .yaticker_pb2 import yaticker

try:
    import thread
except ImportError:
    import _thread as thread


class YLiveTicker:
    def __init__(
        self,
        on_ticker=None,
        ticker_names=["AMZN"],
        on_error=None,
        on_close=None,
        enable_socket_trace=False,
    ):

        self.symbol_list = dict()
        self.symbol_list["subscribe"] = ticker_names

        websocket.enableTrace(enable_socket_trace)

        self.on_ticker = on_ticker
        self.on_custom_close = on_close
        self.on_custom_error = on_error

        self.yaticker = yaticker()
        
        # Cache to store OHLC data from snapshot messages
        # This helps preserve OHLC values when Yahoo doesn't send them in every message
        self.ohlc_cache = {}

        self.ticker_names = ticker_names
        
        self.ws = websocket.WebSocketApp(
            "wss://streamer.finance.yahoo.com/",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.on_open = self.on_open
        self.ws.run_forever()
    
    def get_decimal_places(self, ticker_id, quote_type):
        """
        Determine decimal places based on ticker and quote type:
        - 5 decimals: Currencies with USD, GBP, CHF, CAD as counter currency
        - 3 decimals: Currencies with JPY as counter currency
        - 2 decimals: Commodities and CFD indices
        - No formatting: Everything else (stocks, etc.)
        """
        # Check if it's a currency pair (ends with =X)
        if ticker_id.endswith("=X"):
            # Extract the quote currency (last 3-4 characters before =X)
            # Format: BASEQUOTE=X (e.g., EURUSD=X, USDJPY=X)
            base_quote = ticker_id[:-2]  # Remove =X
            # Get last 3 characters (the quote currency)
            if len(base_quote) >= 3:
                quote_currency = base_quote[-3:].upper()
                # Check for USD, GBP, CHF, CAD (5 decimals)
                if quote_currency in ["USD", "GBP", "CHF", "CAD"]:
                    return 5
                # Check for JPY (3 decimals)
                elif quote_currency == "JPY":
                    return 3
        
        # Check if it's a commodity (quoteType 23)
        if quote_type == 23:  # COMMODITY
            return 2
        
        # Check if it's an index (quoteType 9) or CFD index (starts with ^)
        if quote_type == 9 or ticker_id.startswith("^"):
            return 2
        
        # Default: no formatting (return None)
        return None
    
    def format_price(self, value, decimal_places):
        """Format price value to specified decimal places, or return as-is if None"""
        if value is None:
            return None
        if decimal_places is None:
            return value
        return round(value, decimal_places)

    def on_message(self, ws, message):
        message_bytes = base64.b64decode(message)
        self.yaticker.ParseFromString(message_bytes)
        
        # Convert the Unix timestamp to a human-readable format
        timestamp_ms = self.yaticker.time
        if timestamp_ms and timestamp_ms > 0:
            timestamp_str = datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamp_str = "N/A"
        
        # Yahoo Finance websocket streaming messages primarily contain real-time price updates
        # OHLC data (openPrice, dayHigh, dayLow, previousClose) may only be sent in:
        # 1. Initial snapshot messages when you first connect
        # 2. Periodic updates (not every price tick)
        # We cache OHLC values from messages that contain them, and update day's high/low
        # from streaming prices to maintain accurate OHLC data
        
        ticker_id = self.yaticker.id
        
        # Initialize cache for this ticker if not exists
        if ticker_id not in self.ohlc_cache:
            self.ohlc_cache[ticker_id] = {
                "open": None,
                "high": None,
                "low": None,
                "previousClose": None
            }
        
        # Update cache with OHLC values from Yahoo if they're provided (non-zero)
        # Yahoo sends these in snapshot messages, not in every price update
        if self.yaticker.openPrice and self.yaticker.openPrice != 0.0:
            self.ohlc_cache[ticker_id]["open"] = self.yaticker.openPrice
        if self.yaticker.dayHigh and self.yaticker.dayHigh != 0.0:
            self.ohlc_cache[ticker_id]["high"] = self.yaticker.dayHigh
        if self.yaticker.dayLow and self.yaticker.dayLow != 0.0:
            self.ohlc_cache[ticker_id]["low"] = self.yaticker.dayLow
        if self.yaticker.previousClose and self.yaticker.previousClose != 0.0:
            self.ohlc_cache[ticker_id]["previousClose"] = self.yaticker.previousClose
        
        # Update day's high/low from streaming price if available
        current_price = self.yaticker.price
        if current_price and current_price > 0:
            cached = self.ohlc_cache[ticker_id]
            # Update high if current price is higher
            if cached["high"] is None or current_price > cached["high"]:
                cached["high"] = current_price
            # Update low if current price is lower
            if cached["low"] is None or current_price < cached["low"]:
                cached["low"] = current_price
            # Set open to first price we see if not already set
            if cached["open"] is None:
                cached["open"] = current_price
        
        # Use cached OHLC values (fallback to Yahoo's values if cache not set)
        cached = self.ohlc_cache[ticker_id]
        
        # Determine decimal places based on ticker and quote type
        decimal_places = self.get_decimal_places(ticker_id, self.yaticker.quoteType)
        
        # Get raw OHLC values
        open_price = cached["open"] if cached["open"] is not None else (self.yaticker.openPrice if self.yaticker.openPrice != 0.0 else None)
        high_price = cached["high"] if cached["high"] is not None else (self.yaticker.dayHigh if self.yaticker.dayHigh != 0.0 else None)
        low_price = cached["low"] if cached["low"] is not None else (self.yaticker.dayLow if self.yaticker.dayLow != 0.0 else None)
        prev_close = cached["previousClose"] if cached["previousClose"] is not None else (self.yaticker.previousClose if self.yaticker.previousClose != 0.0 else None)
        
        # Format all price-related fields with appropriate decimal places
        data = {
                "id": ticker_id,
                "exchange": self.yaticker.exchange,
                "quoteType": self.yaticker.quoteType,
                "price": self.format_price(current_price, decimal_places),
                "timestamp": timestamp_str,
                "marketHours": self.yaticker.marketHours,
                "changePercent": self.yaticker.changePercent,
                "dayVolume": self.yaticker.dayVolume,
                "change": self.format_price(self.yaticker.change, decimal_places),
                "priceHint": self.yaticker.priceHint,
                # OHLC data - formatted with appropriate decimal places
                "open": self.format_price(open_price, decimal_places),
                "high": self.format_price(high_price, decimal_places),
                "low": self.format_price(low_price, decimal_places),
                "close": self.format_price(current_price, decimal_places),  # Current price is the last/close price
                "previousClose": self.format_price(prev_close, decimal_places)
            }
        
        if self.on_ticker is None:
            print(json.dumps(data))
        else:
            self.on_ticker(ws, data)

    def on_error(self, ws, error):
        if self.on_custom_error is None:
            writeline(error)
        else:
            self.on_custom_error(error)

    def on_close(self, ws):
        if self.on_custom_close is None:
            writeline("### connection is closed ###")
        else:
            self.on_custom_close()

    def on_open(self, ws):
        def run(*args):
            self.ws.send(json.dumps(self.symbol_list))

        thread.start_new_thread(run, ())
        writeline("### connection is open ###")
