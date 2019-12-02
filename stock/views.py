from django.shortcuts import render, redirect
from django.utils import timezone
import os
from .models import Post
from django.http import HttpResponse
import pandas_datareader as web
from .forms import StockForm
from .forms import UserForm
from .forms import PersonWant
from .forms import PortForm
import pandas as pd
import time
from django.shortcuts import render, HttpResponse, render_to_response
from .models import Question
from .models import Choice
from .models import Person
from .models import Reco
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login


def index1(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    form = StockForm(request.POST)

    time.sleep(2.0)
    a = form['i'].value()

    return render(request, 'stock/index1.html', {'posts': posts,
                                                    'form': form,
                                                    'a':a, })
                                                    # 'df':df,
                                                    # 'context':context})

def index2(request):
    form = StockForm(request.POST)
    return render(request, 'stock/index2.html', {'form': form})


def index2_5(request):
    form = StockForm(request.POST)
    a = form['i'].value()
    df = Post.stock_price_df(a)
    df15 = df[:15]
    context = df15.to_html().replace('border="1"', 'border="0"')
    # Post.stock_chart(a)
    # Post.profit(a)
    # img = 'stock/%s' % a
    # preimg1W = 'stock/preimg/%s_1W' % a + '_pre'
    # preimg15D = 'stock/preimg/%s_15D' % a + '_pre'
    listC = df15['Close'].values.tolist()
    listC = list(map(float, listC))
    min1 = min(listC) * 0.98
    max1 = max(listC)  * 1.02
    futurerate7, list7, futurerate15, list15, futurerate20, list20, name = Post.profit(a)
    min71 = min(list7)
    max71 = max(list7)
    min151 = min(list15)
    max151 = max(list15)
    min201 = min(list20)
    max201 = max(list20)


    return render(request, 'stock/index2_5.html', {'a': a,
                                                   'listC': listC,
                                                   'min1': min1,
                                                   'max1': max1,
                                                   'min71': min71,
                                                   'max71': max71,
                                                   'list7': list7,
                                                   'futurerate7': futurerate7,
                                                   'min151': min151,
                                                   'max151': max151,
                                                   'list15': list15,
                                                   'futurerate15': futurerate15,
                                                   'min201': min201,
                                                   'max201': max201,
                                                   'list20': list20,
                                                   'futurerate20': futurerate20,
                                                   'context': context,
                                                   'name': name})


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('index3_5')
        else:
            return HttpResponse('사용자명이 이미 존재합니다.')
    else:
        form = UserForm()
        return render(request, 'stock/index2_9.html', {'form': form})

#
# def post_list(request):
#     login_form = PersonForm(request.POST)
#     a = login_form['username'].value()
#     form = StockForm(request.POST)
#     b = form['i'].value()
#     # b = login_form['id'].value()
#     # c = login_form['password'].value()
#     return render(request, 'stock/post_list.html', {'a': a,
#                                                     'b': b})
#                                                     # 'id': b,
#                                                     # 'password': c})
#


def index3(request):
    question1 = Question.objects.get(pk=1)
    question2 = Question.objects.get(pk=2)
    question3 = Question.objects.get(pk=3)
    question4 = Question.objects.get(pk=4)
    question5 = Question.objects.get(pk=5)
    question6 = Question.objects.get(pk=6)
    question7 = Question.objects.get(pk=7)

    if 'wedding' in request.POST:
        Person.port = 'wedding'
        Person.wantmoney = 5000
    elif 'car' in request.POST:  # You can use else in here too if there is only 2 submit types.
        Person.port = 'car'
        Person.wantmoney = 3000
    elif 'home' in request.POST:  # You can use else in here too if there is only 2 submit types.
        Person.port = 'home'
        Person.wantmoney = 30000
    elif 'retirement' in request.POST:  # You can use else in here too if there is only 2 submit types.
        Person.port = 'retirement'
        Person.wantmoney = 50000
    elif 'travel' in request.POST:  # You can use else in here too if there is only 2 submit types.
        Person.port = 'travel'
        Person.wantmoney = 500
    elif 'installment' in request.POST:  # You can use else in here too if there is only 2 submit types.
        Person.port = 'installment'
        Person.wantmoney = 10000


    personwant = PersonWant(request.POST)


    return render(request, 'stock/index3.html', {'question1': question1,
                                                 'question2': question2,
                                                 'question3': question3,
                                                 'question4': question4,
                                                 'question5': question5,
                                                 'question6': question6,
                                                 'question7': question7,
                                                 'personwant': personwant})

def index3_5(request):
    return render(request, 'stock/index3_5.html', {})



def index4(request): # Use the Pandas Manager
    question1 = get_object_or_404(Question, pk=1)
    selected_choice1 = question1.choice_set.get(pk=request.POST['choice1'])
    question2 = get_object_or_404(Question, pk=2)
    selected_choice2 = question2.choice_set.get(pk=request.POST['choice2'])
    question3 = get_object_or_404(Question, pk=3)
    selected_choice3 = question3.choice_set.get(pk=request.POST['choice3'])
    question4 = get_object_or_404(Question, pk=4)
    selected_choice4 = question4.choice_set.get(pk=request.POST['choice4'])
    question5 = get_object_or_404(Question, pk=5)
    selected_choice5 = question5.choice_set.get(pk=request.POST['choice5'])
    question6 = get_object_or_404(Question, pk=6)
    selected_choice6 = question6.choice_set.get(pk=request.POST['choice6'])
    question7 = get_object_or_404(Question, pk=7)
    selected_choice7 = question7.choice_set.get(pk=request.POST['choice7'])


    if str(selected_choice1) == "19세 이하":
        Person.person += 4
    elif str(selected_choice1) == "20세~40세":
        Person.person += 4
    elif str(selected_choice1) == "41세~50세":
        Person.person += 3
    elif str(selected_choice1) == "51세~60세":
        Person.person += 2
    elif str(selected_choice1) == "61세 이상":
        Person.person += 1

    if str(selected_choice2) == '6개월 이내':
        Person.wantperiod = 180
        Person.person += 1
    elif str(selected_choice2) == '6개월 이상~1년 이내':
        Person.wantperiod = 360
        Person.person += 2
    elif str(selected_choice2) == '1년 이상~2년 이내':
        Person.wantperiod = 720
        Person.person += 3
    elif str(selected_choice2) == '2년 이상~3년 이내':
        Person.wantperiod = 1080
        Person.person += 4
    elif str(selected_choice2) == '3년 이상':
        Person.wantperiod = 1300
        Person.person += 5

    if str(selected_choice3) == "은행의 예·적금, 국채, 지방채, 보증채, MMF, CMA 등":
        Person.person += 1
    elif str(selected_choice3) == "금융채, 신용도가 높은 회사채, 채권형펀드, 원금보존추구형ELS 등":
        Person.person += 2
    elif str(selected_choice3) == "신용도 중간 등급의 회사채, 원금의 일부만 보장되는 ELS, 혼합형펀드 등":
        Person.person += 3
    elif str(selected_choice3) == "신용도가 낮은 회사채, 주식, 원금이 보장되지 않는 ELS, 시장수익률 수준의 수익을 추구하는 주식형펀드 등":
        Person.person += 4
    elif str(selected_choice3) == "ELW, 선물옵션, 시장수익률 이상의 수익을 추구하는 주식형펀드, 파생상품에 투자하는 펀드, 주식 신용거래 등":
        Person.person += 5

    if str(selected_choice4) == "[매우 낮은 수준] 투자의사 결정을 스스로 내려본 경험이 없는 정도":
        Person.person += 1
    elif str(selected_choice4) == "[낮은 수준] 주식과 채권의 차이를 구별할 수 있는 정도":
        Person.person += 2
    elif str(selected_choice4) == "[높은 수준] 투자할 수 있는 대부분의 금융상품의 차이를 구별할수 있는 정도":
        Person.person += 3
    elif str(selected_choice4) == "[매우 높은 수준] 금융상품을 비롯하여 모든 투자대상 상품의 차이를 이해할 수 있는 정도":
        Person.person += 4

    if str(selected_choice5) == "10% 이내":
        Person.person += 5
    elif str(selected_choice5) == "10% 이상~20% 이내":
        Person.person += 4
    elif str(selected_choice5) == "20% 이상~30% 이내":
        Person.person += 3
    elif str(selected_choice5) == "30% 이상~40% 이내":
        Person.person += 2
    elif str(selected_choice5) == "40% 이상":
        Person.person += 1

    if str(selected_choice6) == "현재 일정한 수입이 발생하고 있으며, 향후 현재 수준을 유지하거나 증가할 것으로 예상된다.":
        Person.person += 3
    elif str(selected_choice6) == "현재 일정한 수입이 발생하고 있으나, 향후 감소하거나 불안정할 것으로 예상된다.":
        Person.person += 2
    elif str(selected_choice6) == "현재 일정한 수입이 없으며, 연금이 주수입원이다.":
        Person.person += 1

    if str(selected_choice7) == "무슨 일이 있어도 투자원금은 보전되어야 한다.":
        Person.person -= 2
    elif str(selected_choice7) == "10% 미만까지는 손실을 감수할 수 있을 것 같다.":
        Person.person += 2
    elif str(selected_choice7) == "20% 미만까지는 손실을 감수할 수 있을 것 같다.":
        Person.person += 4
    elif str(selected_choice7) == "기대수익이 높다면 위험이 높아도 상관하지 않겠다.":
        Person.person += 6

    if Person.person > 0:
        Person.person = (Person.person / 32) * 100
    else: Person.person = 10


    if float(Person.person) < 20:
        Person.type = 'A'
        Person.t = '안정형'
        Person.know = '다소부족'
        Person.risk = 0.15
        Person.ju1rate = 0.15
        Person.ju2rate = 0.15
        Person.ju3rate = 0.7
    if float(Person.person) >= 20 and float(Person.person) < 40.0:
        Person.type = 'B'
        Person.t = '안정추구형'
        Person.know = '적절'
        Person.risk = 0.3
        Person.ju1rate = 0.2
        Person.ju2rate = 0.2
        Person.ju3rate = 0.6
    if float(Person.person) >= 40 and float(Person.person) < 60.0:
        Person.type = 'C'
        Person.t = '위험중립형'
        Person.know = '풍부'
        Person.risk = 0.4
        Person.ju1rate = 0.25
        Person.ju2rate = 0.25
        Person.ju3rate = 0.5
    if float(Person.person) >= 60 and float(Person.person) < 80.0:
        Person.type = 'D'
        Person.t = '적극투자형'
        Person.know = '매우풍부'
        Person.risk = 0.5
        Person.ju1rate = 0.35
        Person.ju2rate = 0.4
        Person.ju3rate = 0.25
    if float(Person.person) >= 80:
        Person.type = 'E'
        Person.t = '공격투자형'
        Person.know = '전문가'
        Person.risk = 0.6
        Person.ju1rate = 0.4
        Person.ju2rate = 0.35
        Person.ju3rate = 0.25

    personwant = PersonWant(request.POST)
    startmoney = personwant['startmoney'].value()

    if Person.risk == 0:
        Person.risk = 0.1


    Person.wantrate = Person.wantmoney / float(startmoney) * 100 / Person.wantperiod
    # Person.wantmoney
    # startmoney = int(startmoney)
    # Person.wantperio

    if Person.wantperiod == 0 :
        Person.wantperiod = 100

    if Person.risk == 0:
        Person.risk = 0.1
    risk =Person.risk

    df71, df72, df73 = Reco.reco7(risk, Person.wantrate)
    df151, df152, df153 = Reco.reco15(risk, Person.wantrate)
    df201, df202, df203 = Reco.reco20(risk, Person.wantrate)

    result = df71.append(df151)
    result = result.append(df201)
    result = result.sort_values(["pro"], ascending=[False])
    result1 = result[:1]

    result = df72.append(df152)
    result = result.append(df202)
    result = result.sort_values(["pro"], ascending=[False])
    result2 = result[:1]

    result = df73.append(df153)
    result = result.append(df203)
    result = result.sort_values(["pro"], ascending=[False])
    result3 = result[:1]

    result = result1.append(result2)
    result = result.append(result3)

    UP_FOLDER = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
    codelist = os.path.join(UP_FOLDER, 'static\\stock\\Data\\codelist-1.xlsx')
    codelist1 = pd.read_excel(codelist)
    codelist = codelist1[['종목코드', '종목명']]

    ch = result.loc[result['high'] == 'h', 'codelist'].values[0]
    nameh = codelist[codelist['종목코드'] == ch]['종목명'].values[0]
    termh = result.loc[result['high'] == 'h', 'term'].values[0]
    cm = result.loc[result['high'] == 'm', 'codelist'].values[0]
    namem = codelist[codelist['종목코드'] == cm]['종목명'].values[0]
    termm= result.loc[result['high'] == 'm', 'term'].values[0]
    cl = result.loc[result['high'] == 'l', 'codelist'].values[0]
    namel = codelist[codelist['종목코드'] == cl]['종목명'].values[0]
    terml=result.loc[result['high'] == 'l', 'term'].values[0]

    try:
        contexth = 0
        listCh = 0
        min1h = 0
        max1h = 0
        Person.ju1 = 0
        df = Post.stock_price_df(ch)
        df15 = df[:15]
        contexth = df15.to_html().replace('border="1"', 'border="0"')
        listCh = df15['Close'].values.tolist()
        listCh = list(map(float, listCh))
        min1h = min(listCh) * 0.98
        max1h = max(listCh) * 1.02
        Person.ju1 = int(int(startmoney) * Person.ju1rate / float(listCh[-1]/10000))
    except:
        pass

    try:
        contextm = 0
        listCm = 0
        min1m = 0
        max1m = 0
        Person.ju2 = 0
        df = Post.stock_price_df(cm)
        df15 = df[:15]
        contextm = df15.to_html().replace('border="1"', 'border="0"')
        listCm = df15['Close'].values.tolist()
        listCm = list(map(float, listCm))
        min1m = min(listCm) * 0.98
        max1m = max(listCm) * 1.02
        Person.ju2 = int(int(startmoney) * Person.ju2rate / float(listCm[-1]/10000))
    except:
        pass

    try:
        contextl = 0
        listCl = 0
        min1l = 0
        max1l = 0
        Person.ju3 = 0
        df = Post.stock_price_df(cl)
        df15 = df[:15]
        contextl = df15.to_html().replace('border="1"', 'border="0"')
        # Post.stock_chart(a)
        # Post.profit(a)
        # img = 'stock/%s' % a
        # preimg1W = 'stock/preimg/%s_1W' % a + '_pre'
        # preimg15D = 'stock/preimg/%s_15D' % a + '_pre'
        listCl = df15['Close'].values.tolist()
        listCl = list(map(float, listCl))
        min1l = min(listCl) * 0.98
        max1l = max(listCl) * 1.02
        Person.ju3 = int(int(startmoney) * Person.ju3rate / float(listCl[-1]/10000))
    except:
        pass

    Person.ju1rate = int(Person.ju1rate * 100)
    Person.ju2rate = int(Person.ju2rate * 100)
    Person.ju3rate = int(Person.ju3rate * 100)
    r = int(Person.wantrate * 365 / 52) + 0.3

    return render(request, 'stock/index4.html', { 'contexth': contexth,
                                                    'contextm':contextm,
                                                    'contextl':contextl,
                                                    'listCh':listCh,
                                                    'listCm':listCm,
                                                    'listCl':listCl,
                                                    'max1h': max1h,
                                                    'min1h':min1h,
                                                    'max1m':max1m,
                                                    'min1m':min1m,
                                                    'max1l':max1l,
                                                    'min1l':min1l,
                                                    'ju1': Person.ju1,
                                                    'ju2': Person.ju2,
                                                    'ju3': Person.ju3,
                                                    't': Person.t,
                                                    'know': Person.know,
                                                  'nameh':nameh,
                                                  'namem':namem,
                                                  'namel': namel,
                                                  'ch': ch,
                                                  'cm': cm,
                                                  'cl': cl,
                                                  'ju1rate': Person.ju1rate,
                                                  'ju2rate': Person.ju2rate,
                                                  'ju3rate': Person.ju3rate,
                                                  'startmoney':startmoney,
                                                  'wantrate': r,
                                                  'termh':termh,
                                                  'termm':termm,
                                                  'terml':terml,
                                                 })
        # 'person': person.person,
        #                                            'type': person.type})




#
# def index4(request):
#
#     return render(request, 'stock/index4.html', {})
#
#







# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # 에러 메세지와 함께 폼을 다시 디스플레이합니다.
#         return render(request, 'stock/index3.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # POST 데이터 처리를 정상적으로 마친 뒤에는 항상 HttpResponseRedirect를 리턴합니다.
#         # 이 방법을 통해 유저가 브라우저의 "뒤로가기"을 눌렀을 때
#         # 데이터가 두 번 저장되는 것을 방지할 수 있습니다.
#         return HttpResponseRedirect(reverse('stock:results', args=(question.id,)))








