


from django.db import models
from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser
from django.utils.timezone import now
from datetime import date

# Create your models here.
#Create your customuser model here
class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password must be provided')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,email,password,**extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email,password,**extra_fields)

#Create your user model here

class User(AbstractBaseUser,PermissionsMixin):
    #AbstractBaseUser has password,last_login,is_active by default
    username=None
    email=models.EmailField(db_index=True,unique=True,max_length=254)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    date_joined=models.DateTimeField(default=now)
    auth_token=models.CharField(max_length=150)
    is_verified=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now=True)
    is_staff=models.BooleanField(default=False)#must need,otherwise you will not able to login
    is_active=models.BooleanField(default=False)#must need,otherwise you will not able to login
    is_superuser=models.BooleanField(default=False)#This is inherited Permissions

    objects=CustomUserManager()
    # EMAIL_FIELD='email'
    USERNAME_FIELD='email'
    REQUIRED_FIELD = []
    class Meta:
        verbose_name='user'
        verbose_name_plural='users'
    def __str__(self):
        return self.email

class Blog(models.Model):
    author=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    post_id=models.AutoField(primary_key=True)
    slug=models.CharField(max_length=130,blank=True)
    title=models.CharField(max_length=100,null=True)
    description=models.TextField(null=True)
    thumbnail=models.ImageField(default="userprofile.png",upload_to='static',null=True)
    date_created=models.DateField(auto_now=True,null=True)
    viewers = models.TextField(default="", null=True, blank=True)
    numViews = models.IntegerField(default=0)
    def __str__(self):
        return self.title + 'by' + ' ' + self.author.first_name
class BlogComment(models.Model): 
    comment_id=models.AutoField(primary_key=True) 
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,null=True,on_delete=models.CASCADE)
    comment=models.CharField(max_length=250)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)#apne hi comment ko point karega
    comment_datetime=models.DateTimeField(default=now,blank=True)
    def __str__(self):
        return self.comment[0:13] + ' ' + 'By' + ' ' +  self.user.first_name

