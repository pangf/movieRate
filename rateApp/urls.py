__author__ = 'pangsm'
from django.conf.urls import url

from rateApp import views

from rateApp.views import HomePageView,movieDetailView,RateCommentView

urlpatterns = [
        url(r'^$',HomePageView.as_view(),name='index'),
        url(r'^(?P<movie_id>\d+)/$',movieDetailView.as_view(), name='detail'),
        url(r'^addRate/$',views.addRate, name='addRate'),
        url(r'^login/$',views.userLogin,name='login'),
        url(r'^register/$',views.register,name='register'),
        url(r'^test1/$',views.test1,name='test1'),
        url(r'^search/$',views.search,name='search'),
        url(r'^rateView/$',RateCommentView.as_view(),name='rateView'),
        url(r'^rateUsefull/(?P<rate_id>\d+)/$',views.rateUsefull,name='rateUsefull'),
      ]