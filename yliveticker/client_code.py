from yliveticker import YLiveTicker


def printRes(ws, res):
    print(res)


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
