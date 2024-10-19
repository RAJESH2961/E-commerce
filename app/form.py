from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *
#here we are overiding placeholder ans some html content
from django import forms


# method-1 we can use custom stylings like placeholders those stuff in the register/HTML page
# class RegisterForm(UserCreationForm):
#     # here we are getting the defalut django models
#     class Meta:
#         model=User
#         fields=['username', 'email', 'password1', 'password2']

# Method-2 Basis Stuff




# class RegisterForm(UserCreationForm):
#     username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter User Name'}))
#     email=forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Email Name'}))
#     password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password'}))
#     password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))
#     # here we are getting the defalut django models
#     class Meta:
#         model=User
#         fields=['username', 'email', 'password1', 'password2']

    

# Method-3  like here we can control html attributes nothing Difference 

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter User Name',
            'maxlength': '30',
            'minlength': '3',
            'required': True,
            'autofocus': True,
            'title': 'Enter your username',
            'style': ' margin:10px 0px;'
        })
    )
   
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email Address',
            'required': True,
            'title': 'Enter a valid email address',
            'style': 'background-color: white; margin:10px 0px;'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password',
            'required': True,
            'title': 'Enter a secure password',
            'style': 'border: 1px solid #ccc; margin:10px 0px;'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'required': True,
            'title': 'Re-enter your password',
            'style': 'border: 1px solid #ccc; margin:10px 0px;'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['name', 'email', 'message']



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)


from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']
