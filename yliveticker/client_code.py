from yliveticker import YLiveTicker
import json

# Track which tickers we've seen
seen_tickers = set()

# Quote type mapping for readability
QUOTE_TYPE_MAP = {
    0: "NONE",
    5: "ALTSYMBOL",
    7: "HEARTBEAT",
    8: "EQUITY",
    9: "INDEX",
    11: "MUTUALFUND",
    12: "MONEYMARKET",
    13: "OPTION",
    14: "CURRENCY",
    15: "WARRANT",
    17: "BOND",
    18: "FUTURE",
    20: "ETF",
    23: "COMMODITY",
    28: "ECNQUOTE",
    41: "CRYPTOCURRENCY",
    42: "INDICATOR",
    1000: "INDUSTRY"
}


def printRes(ws, res):
    ticker_id = res.get("id", "UNKNOWN")
    quote_type = res.get("quoteType", -1)
    price = res.get("price", 0)
    quote_type_name = QUOTE_TYPE_MAP.get(quote_type, f"TYPE_{quote_type}")
    
    # Track seen tickers
    if ticker_id not in seen_tickers:
        seen_tickers.add(ticker_id)
        print(f"\n[+] NEW TICKER SUBSCRIBED: {ticker_id} (Type: {quote_type_name})")
    
    # Show all messages with basic info
    print(f"[{ticker_id}] {quote_type_name} | Price: {price} | Time: {res.get('timestamp')}")
    
    # Print full details for non-heartbeat messages with valid data
    if quote_type != 7 and (price != 0.0 or quote_type == 9):  # Show indexes even if price is 0
        print(json.dumps(res, indent=2))
        print("-" * 50)


def on_close(ws):
    print("bye")


# Connect to Yahoo! Finance and output live data
YLiveTicker(
    on_ticker=printRes,
    on_close=on_close,
    ticker_names=[
        "EURUSD=X",
        "JPY=X",
        "GBPUSD=X",
        "CHF=X",
        "AUDUSD=X",
        "NZDUSD=X",
        "CAD=X",
        "GBPJPY=X",
        "CHFJPY=X",
        "AUDJPY=X",
        "EURGBP=X",
        "GC=F",
        "SI=F",
        "^DJI",
        "^NDX",
        "^GSPC",
        "CL=F",
        "^N225",
        "^HSI"
    ],
)
