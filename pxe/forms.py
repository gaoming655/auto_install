#coding=utf-8
from django import forms
from  models  import * 
from django.utils.translation import ugettext_lazy as _


class login_form(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username: '}))
    passwd = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password: '}))


class edit_form(forms.ModelForm):
    class Meta:
        model = online
        fields = ('ilo_ip','level','kickstart')