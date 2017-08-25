
from django import forms
from rateApp.models import userInf,rateData

class UserCreateForm(forms.ModelForm):
    user_passwd = forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model = userInf
        fields = ('user_id','user_name','user_passwd','user_alias')

class rateInputForm(forms.ModelForm):
    class Meta:
        model=rateData
        fields=["rate_title", "rate_comment", "rate_date", "see_or_not","rate_score"]
        widgets={"rate_comment": forms.Textarea}

class UserRegisterForm(forms.ModelForm):
    user_passwd = forms.CharField(label='Password',widget=forms.PasswordInput)
    class Meta:
        model = userInf
        fields = ('user_name','user_passwd','user_alias')