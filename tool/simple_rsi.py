import requests
import pandas as pd
import time
import webbrowser
import pyupbit
import datetime

access = "Rb0hB7XsGmKwnxxTi1QGryeQUvi0LCVRvwCrxxBe"
secret = "AGg5X755XgfMY2ldhg6fbHv3QpxhxJviDBJE0AwJ"
upbit = pyupbit.Upbit(access, secret)

pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def rsiindex(symbol):
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market": symbol, "count": "500"}
    response = requests.request("GET", url, params=querystring)
    data = response.json()
    df = pd.DataFrame(data)
    df = df.reindex(index=df.index[::-1]).reset_index()
    df['close'] = df["trade_price"]
    def rsi(ohlc: pd.DataFrame, period: int = 14):
        ohlc["close"] = ohlc["close"]
        delta = ohlc["close"].diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="RSI")
    rsi = rsi(df, 14).iloc[-1]
    print('Upbit 1 minute RSI:', rsi)
    time.sleep(1)
    return rsi


b_cnt = -1
e_cnt = -1
b_sell = 0
e_sell = 0
krw = upbit.get_balance("KRW")//4
while(True):
    #b_rsi = rsiindex("KRW-BTC")
    e_rsi = rsiindex("KRW-ETH")
    #if b_cnt == -1: # 시작 전
     #   if b_rsi > 30: # 분석 시작
      #      b_cnt = 0
       #     continue
    if e_cnt == -1: # 시작 전
        if e_rsi > 30: # 분석 시작
            e_cnt = 0
            continue
    
    #if b_cnt == 0: # rsi 28 잡기
     #   if b_rsi < 29:
      #      b_cnt = 1
       #     continue
    if e_cnt == 0:
        if e_rsi < 29:
            e_cnt = 1
            continue
    #if b_cnt == 1:
     #   if b_rsi >= 33:
      #      upbit.buy_market_order("KRW-BTC", krw)
       #     b_sell = 1
        #    b_cnt = 0
    if e_cnt == 1:
        if e_rsi >= 33:
            upbit.buy_market_order("KRW-ETH", krw)
            e_sell = 1
            e_cnt = 0
    #if b_sell == 1:
     #   if b_rsi >= 70:
      #      balance = upbit.get_balance("KRW-BTC")
       #     upbit.sell_market_order("KRW-BTC", balance)
    if e_sell == 1:
        if e_rsi >= 70:
            balance = upbit.get_balance("KRW-ETH")
            upbit.sell_market_order("KRW-ETH", balance)
            e_sell = 0
