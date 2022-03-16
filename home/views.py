
from msilib.schema import ListView
from pyexpat import model
import re
from tempfile import tempdir
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from . forms import LoginForm, UserRegisterForm
from django.core.validators import validate_email
from django.forms import ValidationError
from .templatetags import extra_filter
from .models import *
import uuid
from .helper import send_mail_registration
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView,ListView
# Create your views here.
class Home(ListView):
    template_name='blog.html'
    model=Blog
    paginate_by=4
    ordering=['id']
    paginate_orphans = 1
class Login(LoginView):
    template_name='authentication/login.html'
    authentication_form=LoginForm
    def form_valid(self, form):
        print("Inside Login")
        
        email=self.request.POST.get('username')
   
        if validate_email(email):
                    pass
      
        user_obj=User.objects.filter(email=email).first()
           
        print("Email Exists")
        if user_obj.is_verified!=True:
            messages.success(self.request,'Please check for Your mail to verify')
            return redirect('/login')

        if user_obj.is_verified==True:
            
            print("user is verified")
            auth_login(self.request,form.get_user())
            messages.success(self.request,'Successfully logged in')
            return redirect('/')
               
        else: 
            messages.success(self.request,'Account has not been verified')
            return redirect('/login')
     
        

class Logout(LogoutView):
    template_name='authentication/logout.html'
    success_url='/'



class Register(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('token-send')
    template_name='authentication/sign_up.html'
    def form_valid(self, form):
        form.is_staff=True
        form.is_active=True
        messages.success(self.request, f'Account created successfully')
        return super().form_valid(form)

class Search(TemplateView):
    template_name='blog.html'

class ConfirmLogout(TemplateView):
    template_name='authentication/logout.html'    

class TokenSend(TemplateView):
    template_name='authentication/token_send.html'

class AccountVerify(TemplateView):
    # model=User
    template_name='authentication/verify_account.html'
    def get_context_data(self, **kwargs):
        token=self.kwargs['auth_token']
        print(token)
        user = User.objects.get(auth_token=kwargs['auth_token'])
        user.is_verified=True
        user.save()
        messages.success(self.request,"Your account has been verified")
       
        
        
        #do something with this user
    