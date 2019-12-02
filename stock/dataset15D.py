import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

import sqlite3

look_back = 30
def create_dataset(dataset, look_back = 30):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1 - 15):
        a = dataset[i:(i + look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back + 15][0])
    return np.array(dataX), np.array(dataY)

def dataset15D(con, conn, i, look_back=30):

    df_inter = pd.read_sql("SELECT * FROM '%s'" % i, con, index_col=None)
    df_exter = pd.read_sql("SELECT * FROM 'external'", conn, index_col=None)

    df = pd.merge(df_inter, df_exter, on=['Date'], how='left')
    # df = df_inter
    df = df.sort_values(["Date"], ascending=[False])
    df = df.reset_index(drop=True)
    df.columns

    df = df[['Date','종목코드','종목명','Close','Volume','PER','EPS','시가총액','상장주식수','배당수익률','외국인보유수량',
            '환율-KRW/USD(매매기준율)','시장금리-콜금리(전체거래)','경기종합지수-동행종합지수',
            '수출금액총지수','수입금액총지수','생산자물가지수-한국','소비자물가지수-한국','Kospi','Nas', 'S&P']]

    pandf = df.iloc[:,3:]
    # pandf = df.iloc[:, 6:7]

    pandf = pandf.fillna(method='bfill')
    a = pandf.dropna()
    a = a.reset_index(drop=True)

    if len(pandf.dropna()) == 0:
        pandf = pandf.drop(pandf.iloc[:, 2:4], axis=1)
        pandf = pandf.fillna(method='bfill')
        pandf = pandf.dropna()
        pandf = pandf.reset_index(drop=True)
    else: pandf = a


    # normalization

    nparr = pandf.values[::-1]
    nparr1 = pandf['Close'].values[::-1]
    nparr1 = nparr1.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    nptf = scaler.fit_transform(nparr)
    nptf1 = scaler.fit_transform(nparr1)

    # split train, test
    train_size = int(len(nptf) * 0.95)
    train, test = nptf[0:train_size], nptf[train_size:len(nptf)]

    # create dataset for learning
    look_back = look_back

    testX, testY = create_dataset(test, look_back)
    testY = testY.reshape(-1, 1)


    return testX, testY, scaler

