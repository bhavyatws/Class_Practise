from django.contrib.auth.forms import UserCreationForm
from . models import  User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', widget=forms.TextInput(

        attrs={'auto_focus': True, 'class': 'form-control',

               'placeholder': 'Enter Username or Email',



               }))
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current_password',
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )


# Creating Form for Registration
# from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

# class CommentForm(forms.Form):
#     comment = forms.CharField(widget=forms.Textarea(attrs={
#         'class': 'form-control',
#         'placeholder': 'Enter Comment here',
#         'cols': '5',
#         'rows': '3'

#     }))
#     post_id = forms.CharField(widget=forms.HiddenInput())
#     parent_Sno = forms.CharField(widget=forms.HiddenInput())


# class ReplyCommentForm(forms.Form):
#     reply = forms.CharField(widget=forms.Textarea(attrs={
#         'class': 'form-control',
#         'placeholder': 'Enter Comment here',
#         'cols': '5',
#         'rows': '3'

#     }))
