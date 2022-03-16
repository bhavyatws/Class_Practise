
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UsernameField
from django.utils.translation import gettext_lazy as _

class LoginForm(AuthenticationForm):
    username=forms.CharField(label='Username or Email',widget=forms.TextInput(
       
        attrs={'auto_focus':True,'class':'form-control',
    
    'placeholder':'Enter Username or Email',
   
    

    }))
    password=forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete':'current_password',
            'class':'form-control',
            'placeholder':'Enter Password'
        })
    )
    # def set_field_html_name(cls, new_name):
    #     """
    #     This creates wrapper around the normal widget rendering, 
    #     allowing for a custom field name (new_name).
    #     """
    #     old_render = cls.widget.render
    #     def _widget_render_wrapper(name, value, attrs=None):
    #         return old_render(new_name, value, attrs)

    #     cls.widget.render = _widget_render_wrapper
    # # After creating the field, call the wrapper with your new field name.
    # set_field_html_name(username, 'email')

#Creating Form for Registration
# from django.contrib.auth.models import User
from . models import User

from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
      model = User
      fields = ['email', 'first_name','last_name']
      widgets={
          'email':forms.EmailInput(attrs={'class':'form-control'})
      }