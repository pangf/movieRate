from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible  #this is for chinese compatible
# movie information model
class movieInf(models.Model):
    TYPE_CHOICES = (
        ('Action','action movie'), # First value is stored in db, the second is descriptive
        ('Comedy', 'comedy movie'),
        ('History', 'historical movie'),
        ('Cartoon', 'cartoon movie'),
        ('Document','documentary movie'),
        ('Other','other movie'),
    )
    movie_id = models.IntegerField(primary_key=True)
    movie_name = models.CharField(max_length=96)
    movie_des = models.CharField(max_length=400)
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=200)
    writers = models.CharField(max_length=200)
    movie_date =  models.DateField()
    movie_type = models.CharField(max_length=10,choices=TYPE_CHOICES, default='Action')
    language = models.CharField(max_length=10)
    country = models.CharField(max_length=32)
    length = models.IntegerField()
    alias = models.CharField(max_length=96)
    currentRateValue = models.IntegerField(default=0)
    movie_image = models.ImageField(upload_to='photos', null=True, blank=True)

    def __str__(self):
        return (self.movie_name)

@python_2_unicode_compatible
class userInf(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=32)
    user_passwd = models.CharField(max_length=32)
    user_alias = models.CharField(max_length=32)

    def __str__(self):
        return(self.user_alias)

@python_2_unicode_compatible
class rateData(models.Model):
    rate_id = models.IntegerField(primary_key=True)
    rate_title = models.CharField(max_length=64)
    movie = models.ForeignKey(movieInf,default='')
    user = models.ForeignKey(userInf,default='')
    rate_score = models.IntegerField()
    rate_comment = models.CharField(max_length=400)
    see_or_not = models.BooleanField()
    rate_date = models.DateField()
    rateusefull = models.IntegerField()
    rateuseless = models.IntegerField()

    def __str__(self):
        return (self.rate_title)



