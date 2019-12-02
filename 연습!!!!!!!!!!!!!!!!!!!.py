

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import sqlite3
import pandas_datareader as web
import datetime

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

    # reshape input to be [samples, time steps, features]


    return testX, testY, scaler

con = sqlite3.connect("D://lec403//로보플젝데이터//stock_notna_ffill.db")
conn = sqlite3.connect("D://lec403//로보플젝데이터//stock_external_최종.db")

code = '000020'


Xtest, Ytest, scaler = dataset1W(con, conn, code, look_back=25)
model7 = load_model("D://lec403//로보플젝데이터//모델1W//000020_1W.h5")

x = Xtest[len(Xtest) - 7:]
y = Post.stock_chart(code)
y = y.values.tolist()
pre = model7.predict(x)
Pre = scaler.inverse_transform(pre)
past7 = y[0]
cur7 = y[-1]
gap = Pre[-1] - Pre[0]
future7 = cur7 + gap
future7 = round(future7[0], 0)
futurerate7 = float(future7 / cur7)
futurerate7 = round(futurerate7, 2)
list7 = []

list7 = [float(past7), float(cur7), float(future7)]







class Post():

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def stock_price_df(code):
        date = datetime.datetime.today()
        start = date - datetime.timedelta(15)
        date = date.date()
        date = date.strftime('%Y-%m-%d')
        # date = date.replace("-", "", 2)
        start = start.date()
        start = start.strftime('%Y-%m-%d')
        df = web.DataReader('%s.KS' % code, 'yahoo', start, date)
        return df

    def stock_chart(code):
        UP_FOLDER = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
        img = os.path.join(UP_FOLDER, 'static\\stock\\%s.png' % code)
        tdate = datetime.datetime.today()
        yesterday = tdate - datetime.timedelta(1)
        yesterday = yesterday.date()
        yesterday = yesterday.strftime('%Y-%m-%d')
        start = tdate - datetime.timedelta(7)
        start = start.date()
        start = start.strftime('%Y-%m-%d')
        df = web.DataReader('%s.KS' % code, 'yahoo', start, yesterday)
        return df['Close']


    def profit(code):
        from keras.models import load_model
        # import tensorflow as tf
        # global graph, model
        # graph = tf.get_default_graph()



        UP_FOLDER = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
        codelist = os.path.join(UP_FOLDER, 'static\\stock\\Data\\codelist-1.xlsx')
        con = os.path.join(UP_FOLDER, 'static\\stock\\Data\\stock_notna_ffill.db')
        conn = os.path.join(UP_FOLDER, 'static\\stock\\Data\\stock_external_최종.db')

        codelist1 = pd.read_excel(codelist)
        codelist1 = codelist1['종목코드']
        codelist1 = codelist1.values.tolist()
        con = sqlite3.connect(con)
        conn = sqlite3.connect(conn)
        df = Post.stock_chart(code)
        #
        # profit_list = []
        Xtest, Ytest, scaler = dataset1W(con, conn, code, look_back=25)
        model7 = os.path.join(UP_FOLDER, 'static\\stock\\model1W\\%s_1W.h5' % code)
        img1W = os.path.join(UP_FOLDER, 'static\\stock\\preimg\\%s_1W_pre.png' % code)
        model7 = load_model(model7)
        x = Xtest[len(Xtest) - 7:]
        y = Post.stock_chart(code)
        y = y.values.tolist()
        pre = model7.predict(x)
        Pre = scaler.inverse_transform(pre)
        past7 = y[0]
        cur7 = y[-1]
        gap = Pre[-1] - Pre[0]
        future7 = cur7 + gap
        futurerate7 = float(future7 / cur7)
        futurerate7 = round(futurerate7, 1)
        list7 = []

        list7 = [float(past7), float(cur7), float(future7)]

        # Xtest, Ytest, scaler = dataset15D(con, conn, code, look_back=30)
        # model15 = os.path.join(UP_FOLDER, 'static\\stock\\model15D\\%s_15D.h5' % code)
        # img1W = os.path.join(UP_FOLDER, 'static\\stock\\preimg\\%s_15D_pre.png' % code)
        # model15 = load_model(model15)
        # x = Xtest[len(Xtest) - 15:]
        # pre = model15.predict(x)
        # Pre = scaler.inverse_transform(pre)
        gap = Pre[-1] - Pre[0]
        # pre = [df[-1], df[-1] + gap]
        # profit = Pre[-1] - Pre[0]

        # profit_list.append(profit)
        # profit_df = pd.DataFrame(profit_list)
        # profit_df.to_excel("D://lec403//로보플젝데이터//%s_profit.xlsx" % i)

        return futurerate7, list7