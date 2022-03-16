from distutils.command.install_data import install_data
import imp
from .models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .helper import send_mail_registration
import uuid

#this function run when user created
@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        # Profile.objects.create(user=instance) => if Profile model ma there is user foreign key
        
        email = (instance.email)
        token=str(uuid.uuid4())
        instance.auth_token=token
        instance.is_active=True#making staff true which is default false we have set
        instance.save()
        send_mail_registration(email,token)
        print("Email has n")
        
# This function run when user is updated
'''@receiver(post_save, sender=User)
def new_booking(sender, instance, **kwargs):
    if instance.email:
        email = (instance.email)
        token=str(uuid.uuid4())
        send_mail_registration(email,token, fail_silently=False)'''