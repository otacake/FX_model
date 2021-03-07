import numpy as np
import pandas as pd
import talib

df_USD_JPY = pd.read_csv("USD_JPY.csv")

print(df_USD_JPY.head())

close_value = np.array(df_USD_JPY["終値"])

df_features = pd.DataFrame(index=range(len(df_USD_JPY)),columns=["RSI","MACD","EMA5","EMA20","BBANDS+1d","BBANDS+2d","BBANDS-1d","BBANDS-2d"])

df_features["date"] = df_USD_JPY["日付け"]

df_features["RSI"] = talib.RSI(close_value,timeperiod=14)
df_features["MACD"],_,_ = talib.MACD(close_value,fastperiod=12, slowperiod=26, signalperiod=9)

df_features["EMA5"] = talib.EMA(close_value,timeperiod=5) / close_value
df_features["EMA20"] = talib.EMA(close_value,timeperiod=20) / close_value

upper2,mid,lower2 = talib.BBANDS(close_value, timeperiod=20, nbdevup=3, nbdevdn=3)
upper1,mid,lower1 = talib.BBANDS(close_value, timeperiod=20, nbdevup=2, nbdevdn=2)

df_features["BBANDS+1d"] = upper1 / close_value
df_features["BBANDS+2d"] = upper2 / close_value
df_features["BBANDS-1d"] = lower1 / close_value
df_features["BBANDS-2d"] = lower2 / close_value

df_USD_JPY["comp_ratio"] = df_USD_JPY["前日比%"].apply(lambda x: float(x.replace("%", "")))
df_y = df_USD_JPY["comp_ratio"].shift()

df_features = pd.concat([df_features,df_y],axis=1)
df_features =df_features.dropna(how="any")

df_features["GC/DC"] = df_features["EMA5"] - df_features["EMA20"]
df_features = df_features.rename(columns={"終値":"close_calue"})

del df_features["EMA5"]
del df_features["EMA20"]

print(df_features.head())

df_features.to_csv("features.csv")