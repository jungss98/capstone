import os

from django.db import models
from django.utils import timezone
import pandas as pd
import pandas_datareader as web
from django_pandas.managers import DataFrameManager
import matplotlib.pyplot as plt
import datetime
import sqlite3

from .dataset1W import dataset1W
from .dataset15D import dataset15D
from .dataset20D import dataset20D
from keras import backend as K
import numpy as np
from pandas.plotting import register_matplotlib_converters


import time


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def stock_price_df(code):
        date = datetime.datetime.today()
        start = date - datetime.timedelta(12)
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
        start = tdate - datetime.timedelta(35)
        start = start.date()
        start = start.strftime('%Y-%m-%d')
        df = web.DataReader('%s.KS' % code, 'yahoo', start, yesterday)

        return df['Close']


    def profit(code):
        from keras.models import load_model
        # import tensorflow as tf
        # global graph, model
        # graph = tf.get_default_graph()


        K.clear_session()

        UP_FOLDER = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
        codelist = os.path.join(UP_FOLDER, 'static\\stock\\Data\\codelist-1.xlsx')
        con = os.path.join(UP_FOLDER, 'static\\stock\\Data\\stock_notna_ffill.db')
        conn = os.path.join(UP_FOLDER, 'static\\stock\\Data\\stock_external_최종.db')

        codelist1 = pd.read_excel(codelist)
        codelist = codelist1[['종목코드', '종목명']]
        name = codelist[codelist['종목코드'] == code]['종목명'].values[0]
        # codelist1 = codelist1['종목코드']
        # codelist1 = codelist1.values.tolist()
        con = sqlite3.connect(con)
        conn = sqlite3.connect(conn)
        df = Post.stock_chart(code)

        Xtest, Ytest, scaler = dataset1W(con, conn, code, look_back=25)
        model7 = os.path.join(UP_FOLDER, 'static\\stock\\model1W\\%s_1W.h5' % code)
        model7 = load_model(model7)
        x = Xtest[len(Xtest) - 7:]
        pre = model7.predict(x)
        del model7
        y = Post.stock_chart(code)
        y = y.values.tolist()
        Pre = scaler.inverse_transform(pre)
        past7 = y[7]
        cur7 = y[-1]
        gap = Pre[-1] - Pre[0]
        future7 = cur7 + gap
        future7 = round(future7[0], 0)
        futurerate7 = float(future7 / cur7)
        futurerate7 = round(futurerate7, 3)
        list7 = []
        list7 = [float(past7), float(cur7), float(future7)]

        Xtest, Ytest, scaler = dataset15D(con, conn, code, look_back=30)
        model15 = os.path.join(UP_FOLDER, 'static\\stock\\model15D\\%s_15D.h5' % code)
        model15 = load_model(model15)
        x = Xtest[len(Xtest) - 15:]
        pre = model15.predict(x)
        del model15
        # Ytest = Ytest.reshape(-1,1)
        # Y = scaler.inverse_transform(Ytest)
        # y = y.values.tolist()
        Pre = scaler.inverse_transform(pre)
        past15 = y[15]
        cur15 = y[-1]
        gap = Pre[-1] - Pre[0]
        future15 = cur15 + gap
        future15 = round(future15[0], 0)
        futurerate15 = float(future15 / cur15)
        futurerate15 = round(futurerate15, 3)
        list15 = []
        list15 = [float(past15), float(cur15), float(future15)]

        Xtest, Ytest, scaler = dataset20D(con, conn, code, look_back=60)
        model20 = os.path.join(UP_FOLDER, 'static\\stock\\model20D\\%s_20D.h5' % code)
        model20 = load_model(model20)
        x = Xtest[len(Xtest) - 20:]
        pre = model20.predict(x)
        del model20
        # Ytest = Ytest.reshape(-1, 1)
        # Y = scaler.inverse_transform(Ytest)
        # y = y.values.tolist()
        Pre = scaler.inverse_transform(pre)
        past20 = y[20]
        cur20 = y[-1]
        gap = Pre[-1] - Pre[0]
        future20 = cur20 + gap
        future20 = round(future20[0], 0)
        futurerate20 = float(future20 / cur20)
        futurerate20 = round(futurerate20, 3)
        list20 = []
        list20 = [float(past20), float(cur20), float(future20)]



        # Xtest, Ytest, scaler = dataset15D(con, conn, code, look_back=30)
        # model15 = os.path.join(UP_FOLDER, 'static\\stock\\model15D\\%s_15D.h5' % code)
        # img1W = os.path.join(UP_FOLDER, 'static\\stock\\preimg\\%s_15D_pre.png' % code)
        # model15 = load_model(model15)
        # x = Xtest[len(Xtest) - 15:]
        # pre = model15.predict(x)
        # Pre = scaler.inverse_transform(pre)
        # gap = Pre[-1] - Pre[0]
        # pre = [df[-1], df[-1] + gap]
        # profit = Pre[-1] - Pre[0]

        # profit_list.append(profit)
        # profit_df = pd.DataFrame(profit_list)
        # profit_df.to_excel("D://lec403//로보플젝데이터//%s_profit.xlsx" % i)

        return futurerate7, list7, futurerate15, list15, futurerate20, list20, name

class Reco(models.Model):

    def reco7(risk, rate):
        risk = risk
        UP_FOLDER = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
        pre = os.path.join(UP_FOLDER, 'static\\stock\\Data\\7SCORE입니당.xlsx')
        pro = os.path.join(UP_FOLDER, 'static\\stock\\Data\\7수익률입니당.xlsx')
        pre7 = pd.read_excel(pre, dtype={'codelist': 'str'})
        pro7 = pd.read_excel(pro,dtype={'codelist': 'str'})

        df = pd.merge(pre7, pro7, on=['codelist'], how='right')

        df = df.sort_values(["pre"], ascending=[False])

        df = df.dropna()

        df = df[:int(len(df) * risk)]

        df = df.sort_values(["pro"], ascending=[False])

        df = df.reset_index(drop=True)

        def find_nearest(array, value):
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        dfp = df['pro'].as_matrix()
        s = df[df['pro'] == find_nearest(dfp, rate)].index[0]
        df = df[s - 22: s]

        codelistv = df['codelist'].values.tolist()

        date = datetime.datetime.today()
        start = date - datetime.timedelta(60)
        date = date.date()
        date = date.strftime('%Y-%m-%d')
        # date = date.replace("-", "", 2)
        start = start.date()
        start = start.strftime('%Y-%m-%d')
        df['term'] = 7
        df['var'] = np.nan
        for i in codelistv:
            dfv = web.DataReader('%s.KS' % i, 'yahoo', start, date)
            df.loc[df['codelist'] == i, 'var'] = dfv['Close'].var()

        df = df.sort_values(["var"], ascending=[False])

        df1 = df[:1]
        df2 = df[int(len(df) * 0.33):int(len(df) * 0.33) + 1]
        df3 = df[int(len(df) * 0.66):int(len(df) * 0.66) + 1]

        df1['high'] = 'h'
        df2['high'] = 'm'
        df3['high'] = 'l'

        return df1, df2, df3

    def reco15(risk, rate):
        risk=risk
        UP_FOLDER = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
        pre = os.path.join(UP_FOLDER, 'static\\stock\\Data\\15SCORE입니당.xlsx')
        pro = os.path.join(UP_FOLDER, 'static\\stock\\Data\\15수익률입니당.xlsx')
        pre15 = pd.read_excel(pre, dtype={'codelist': 'str'})
        pro15 = pd.read_excel(pro, dtype={'codelist': 'str'})

        df = pd.merge(pre15, pro15, on=['codelist'], how='right')

        df = df.sort_values(["pre"], ascending=[False])

        df = df.dropna()

        df = df[:int(len(df) * risk)]

        df = df.sort_values(["pro"], ascending=[False])

        df = df.reset_index(drop=True)

        def find_nearest(array, value):
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        dfp = df['pro'].as_matrix()
        s = df[df['pro'] == find_nearest(dfp, rate)].index[0]
        df = df[s - 22: s]

        codelistv = df['codelist'].values.tolist()

        date = datetime.datetime.today()
        start = date - datetime.timedelta(60)
        date = date.date()
        date = date.strftime('%Y-%m-%d')
        # date = date.replace("-", "", 2)
        start = start.date()
        start = start.strftime('%Y-%m-%d')
        df['term'] = 15
        df['var'] = np.nan
        for i in codelistv:
            dfv = web.DataReader('%s.KS' % i, 'yahoo', start, date)
            df.loc[df['codelist'] == i, 'var'] = dfv['Close'].var()

        df = df.sort_values(["var"], ascending=[False])

        df1 = df[:1]
        df2 = df[int(len(df) * 0.33):int(len(df) * 0.33) + 1]
        df3 = df[int(len(df) * 0.66):int(len(df) * 0.66) + 1]

        df1['high'] = 'h'
        df2['high'] = 'm'
        df3['high'] = 'l'

        return df1, df2, df3

    def reco20(risk, rate):
        risk = risk
        UP_FOLDER = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
        pre = os.path.join(UP_FOLDER, 'static\\stock\\Data\\20SCORE입니당.xlsx')
        pro = os.path.join(UP_FOLDER, 'static\\stock\\Data\\20수익률입니당.xlsx')
        pre20 = pd.read_excel(pre, dtype={'codelist': 'str'})
        pro20 = pd.read_excel(pro, dtype={'codelist': 'str'})

        df = pd.merge(pre20, pro20, on=['codelist'], how='right')

        df = df.sort_values(["pre"], ascending=[False])

        df = df.dropna()

        df = df[:int(len(df) * risk)]

        df = df.sort_values(["pro"], ascending=[False])

        df = df.reset_index(drop=True)

        def find_nearest(array, value):
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        dfp = df['pro'].as_matrix()
        s = df[df['pro'] == find_nearest(dfp, rate)].index[0]
        df = df[s - 22: s]

        codelistv = df['codelist'].values.tolist()

        date = datetime.datetime.today()
        start = date - datetime.timedelta(60)
        date = date.date()
        date = date.strftime('%Y-%m-%d')
        # date = date.replace("-", "", 2)
        start = start.date()
        start = start.strftime('%Y-%m-%d')
        df['term'] = 20
        df['var'] = np.nan
        for i in codelistv:
            dfv = web.DataReader('%s.KS' % i, 'yahoo', start, date)
            df.loc[df['codelist'] == i, 'var'] = dfv['Close'].var()

        df = df.sort_values(["var"], ascending=[False])

        df1 = df[:1]
        df2 = df[int(len(df) * 0.33):int(len(df) * 0.33) + 1]
        df3 = df[int(len(df) * 0.66):int(len(df) * 0.66) + 1]

        df1['high'] = 'h'
        df2['high'] = 'm'
        df3['high'] = 'l'

        return df1, df2, df3



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):  # __unicode__ on Python 2
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)

    def __str__(self):  # __unicode__ on Python 2
        return self.choice_text


class Person(models.Model):
    startmoney = 0
    person = 0
    type = 'x'
    port = 'x'
    wantrate = 0
    wantperiod = 0
    wantmoney = 0
    risk = 0
    ju1rate = 0
    ju2rate = 0
    ju3rate = 0
    ju1 = 1
    ju2 = 1
    ju3 = 1
    t = 'x'
    know = 'x'

