import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

import sqlite3

def create_dataset(dataset, look_back = 25):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1 - 15):
        a = dataset[i:(i + look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back + 15][3])
    return np.array(dataX), np.array(dataY)


def dataset1W(con, conn, i, look_back=25):
    df_inter = pd.read_sql("SELECT * FROM '%s'" % i, con, index_col=None)
    df_exter = pd.read_sql("SELECT * FROM 'external'", conn, index_col=None)
    df = pd.merge(df_inter, df_exter, on=['Date'], how='left')
    # df = df_inter
    df = df.sort_values(["Date"], ascending=[False])
    df = df.reset_index(drop=True)
    pandf = df.iloc[:, 3:]
    # pandf = df.iloc[:, 6:7]

    pandf = pandf.fillna(method='bfill')
    a = pandf.dropna()
    a = a.reset_index(drop=True)

    if len(pandf.dropna()) == 0:
        pandf = pandf.drop(pandf.iloc[:, 6:10], axis=1)
        pandf = pandf.dropna()
        pandf = pandf.reset_index(drop=True)
        print("DataFrame is NULL!!!")

    else:
        pandf = a

    nparr = pandf.values[::-1]
    nparr1 = pandf['Close'].values[::-1]
    nparr1 = nparr1.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    nptf = scaler.fit_transform(nparr)
    nptf1 = scaler.fit_transform(nparr1)

    # split train, test
    train_size = int(len(nptf) * 0.95)
    train, test = nptf[0:train_size], nptf[train_size:len(nptf)]

    look_back = look_back
    # create dataset for learning
    testX, testY = create_dataset(test, look_back)
    testY = testY.reshape(-1, 1)


    return testX, testY, scaler