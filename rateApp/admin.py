from __future__ import unicode_literals

from django.contrib import admin
from rateApp.forms import UserCreateForm
from  rateApp.models import movieInf,rateData,userInf

class UserAdmin(admin.ModelAdmin):
    form = UserCreateForm
    fields = ('user_id', 'user_name', 'user_passwd','user_alias')

# Register your models here.
admin.site.register(movieInf)
admin.site.register(rateData)
admin.site.register(userInf,UserAdmin)
