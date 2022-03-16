from django.conf import settings
from django.core.mail import send_mail
def send_mail_registration(email,token):
    subject='Your account need to be verified to login'
    # message=f'Paste the link to verify your account https://shahidblogapp.herokuapp.com/verify/{token}'
    message=f'Paste the link to verify your account http://127.0.0.1:8000/verify-account/{token}'#for local
    email_from=settings.EMAIL_HOST_USER
    recipient=[email]
    #fail_silently=True means on production if by means email does not send 
    #then no error will come otherwise big error comes
    send_mail(subject,message,email_from,recipient,fail_silently=True)

#generating unique slug
import string 
from django.utils.text import slugify 
import random 
  
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size)) 
  
def unique_slug_generator(instance, new_slug = None): #passing instance as param
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.title) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return unique_slug_generator(instance, new_slug = new_slug) 
    return slug 