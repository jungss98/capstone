from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index1, name='index1'),
    path('index1.html', views.index1, name='index1'),
    path('index2.html', views.index2, name='index2'),
    path('index2_5.html', views.index2_5, name='index2_5'),
    path('index2_9.html', views.signup, name='index2_9'),
    path('index3_5.html', views.index3_5, name='index3_5'),
    path('index3.html', views.index3, name='index3'),
    path('index4.html', views.index4, name='index4'),
    # path('post_list.html', views.post_list, name='post_list'),
    path('login.html', auth_views.login,  {'template_name':'stock/login.html'}),
]
# {'template_name':'stock/login.html'}


