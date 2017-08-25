from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from rateApp.models import movieInf,rateData,userInf
from rateApp.forms import rateInputForm,UserRegisterForm
import datetime
from movieRate import settings

from django.utils.encoding import python_2_unicode_compatible
#@python_2_unicode_compatible  #this is for chinese compatible
# Create your views here.


# home page view function
class HomePageView(TemplateView):
    template_name = "rateApp/index.html"
    def get_context_data(self,**kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['movielist'] =  movieInf.objects.all().order_by('movie_name')[:10]
        context['rateList'] = rateData.objects.all().order_by('rate_score')[:10]
        rateList = rateData.objects.all().order_by('rate_score')[:10]
        context['rateList'] = rateList
        return context

#function of view registed user's rate comment
class RateCommentView(TemplateView):
    template_name = "rateApp/rateView.html"
    def get_context_data(self,**kwargs):
        context = super(RateCommentView, self).get_context_data(**kwargs)
        if settings.cur_user_id > 0:
           user = userInf.objects.get(user_id = settings.cur_user_id)
           context['rateList'] = rateData.objects.filter(user=user)
        else:
           context['user_id'] = 0
        context['user_id'] = settings.cur_user_id
        return context

# function for movie detail information view
class movieDetailView(TemplateView):
     template_name = "rateApp/movieDetail.html"
     def get_context_data(self, **kwargs):
         context = super(movieDetailView, self).get_context_data(**kwargs)
         movieID = context['movie_id']
         settings.cur_movie_id = movieID
         context['movielist'] = movieInf.objects.filter(movie_id=movieID)
         return context

# function for add comment of a movie
def addRate(request):
    if settings.cur_user_id==0:
        return HttpResponseRedirect(reverse('rateApp:login'))
    if request.method == 'POST':
       rateList = rateData.objects.all()
       count = rateList.count()
       count += 1
       #create an object of rateData
       movieobj = movieInf.objects.get(movie_id = settings.cur_movie_id)
       userobj = userInf.objects.get(user_id = settings.cur_user_id)
       obj = rateData()
       obj.rate_id = count
       obj.rate_date = datetime.datetime.now()
       obj.rate_comment = request.POST['rateComment']
       obj.rate_title = request.POST['rateTitle']
       obj.rate_score = request.POST['rateScore']
       obj.movie = movieobj
       obj.user = userobj
       try:
          if request.POST['see']:
            obj.see_or_not = True
          else:
            obj.see_or_not = False
       except:
           obj.see_or_not = False
       obj.rateusefull = 0
       obj.rateuseless = 0
      # save the data
       obj.save()
      #set rate score
       rateList = rateData.objects.filter( movie = movieobj)
       v = 0
       if rateList:
         for rateD in rateList:
            v = v+ rateD.rate_score
         v = v/float(str(rateList.count()))
         v = int(v)/10 - 4
         if v < 0 :
             v = 0
       movies = movieInf.objects.filter(movie_id=settings.cur_movie_id)
       for movie in movies:
          movie.currentRateValue = v
          movie.save()  #save the rate score in movieInf

       return HttpResponseRedirect(reverse('rateApp:index'))
    else:
       return render(request, 'rateApp/addRateData.html')
#function for user login
def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usr = user_authenticate(username=username, password=password)
        if usr:
            settings.cur_user_name = usr
            settings.cur_user_id = getUserId(username=username)
            return HttpResponseRedirect(reverse('rateApp:index'))
        else:
            return render(request, 'rateApp/login.html')  # return to login pang
#            return HttpResponse('Your account is disabled.')
    else:
        return render(request, 'rateApp/login.html')

#function for registe a user
def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():
             form.save()
             return HttpResponseRedirect(reverse('rateApp:index'))
    else:
        form=UserRegisterForm()
    return render(request, 'rateApp/register.html', {'form':form})
# function for search
def search(request):
    if request.method=='POST':
         searchStr = request.POST['search_text']
         objs = movieInf.objects.filter(movie_name__contains=searchStr)
         if objs:
             movie_id = objs[0].movie_id
             return render(request, 'rateApp/movieDetail.html', {'movielist': objs})
         else:
            objs = movieInf.objects.filter(actors__contains=searchStr)
            if objs:
                return render(request, 'rateApp/movieDetail.html', {'movielist': objs})
            else:
                return HttpResponseRedirect(reverse('rateApp:index'))

    else:
         return HttpResponseRedirect(reverse('rateApp:index'))


# function for testing
def test1(request):
     response=HttpResponse()
     response.write("This is test.")
     rateList = rateData.objects.all().order_by('rate_score')[:10]
     usrNamelist= []
     movieNameList = []
     count = rateList.count()
     response.write(count)
     response.write(",")
     for i in range( count ):
         obj1 = movieInf.objects.filter( movie_id = rateList[i].movie_id  )
         for d in obj1:
            movieNameList.append(d.movie_name)
            response.write(d.movie_name)
            response.write(",")
         obj2 = userInf.objects.filter( user_id = rateList[i].user_id )
         for d1 in obj2:
            usrNamelist.append(d1.user_alias)
            response.write(d1.user_alias)
            response.write(",")
     for j in range( count ):
        response.write(usrNamelist)
        response.write(",")
        response.write(movieNameList)
     return response

def rateUsefull(request,rate_id):
    obj = rateData.objects.get(rate_id=rate_id)
    if obj:
        obj.rateusefull += 1
        obj.save()
    return HttpResponseRedirect(reverse('rateApp:index'))


# function for determining if the user is volid
def user_authenticate(username,password):
    obj = userInf.objects.filter(user_name=username)
    for usr in obj:
        if usr.user_passwd == password :
            return usr.user_alias   # return the user alias
        else:
            s=''
            return s
# function for getting the user ID useing username
def getUserId(username):
    obj = userInf.objects.filter(user_name=username)
    if obj:
        for usr in obj:
            return usr.user_id   # return the user alias
    else:
        return 0

