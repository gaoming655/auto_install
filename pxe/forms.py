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
        fields = ('ilo_ip','level','kickstart','stripe','service_ip','service_netmask','service_gw')
        widgets ={
            'ilo_ip':forms.TextInput(attrs={'class':'form-control'}),
            'service_ip':forms.TextInput(attrs={'class':'form-control'}),
            'service_gw':forms.TextInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'ilo_ip': {
                'invalid':_("IP地址格式不正确"),
            }
        }