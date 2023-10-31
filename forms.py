from django import forms 

from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import *
from .models import User
from django.forms import ModelForm


class Roomform(ModelForm):
    
    class Meta:
        model=Room
        exclude=['host','participants']

class userupdate(ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'first_name'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'last_name'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}))
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

class updateuser2(ModelForm):
    
    class Meta:
        model=Profile
        fields=['bio','avator']

class Updatemessage(ModelForm):
    class Meta:
        model=Message
        fields='__all__'
    
class addtopicform(ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))

    class Meta:
        model=Topic
        fields=['name']

class passwordchangingform(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'old password'}))
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'new password'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm new password'}))   
    class Meta:
        model=User
        fields=['old_password','new_password1','new_password2']


class signupform(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm password'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}))
   
    class Meta:
        model=User
        fields=['username','password1','password2','email']


class pwresetform(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))


class pwreset(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'new password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm new password'}))   
   
class otpform(forms.Form):
    otp=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'verify otp'}))
    
 