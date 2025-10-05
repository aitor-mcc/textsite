from django.db import models 
from django.contrib.auth.models import AbstractBaseUser 
from django.contrib.auth.models import AbstractUser 
from django.db import models 
from django.utils.translation import gettext as _ 
from functions import * 
from .managers import CustomUserManager 
 
class CustomUser(AbstractUser): 
    email = models.EmailField(_('email address'), unique=True) 
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ('username',) 
 
    objects = CustomUserManager() 
 
    def __str__(self): 
        return self.email 
 
    def create_user(self, email, username, password=None): 
        """ 
        Creates and saves a User with the given email, username, and password. 
        """ 
        if not email: 
            raise ValueError('Users must have an email address') 
        if not username: 
            raise ValueError('Users must have a username address') 
 
        user = self.model( 
            email=CustomUserManager.normalize_email(email), 
            username = username, 
        ) 
     
        user.set_password(password) 
        user.save(using=self._db) 
         
        return user 
     
 
class key(models.Model): 
    uuid = models.OneToOneField(CustomUser, verbose_name=_('UUID'), primary_key=True, on_delete = models.CASCADE) 
    public_exponent = models.IntegerField() 
    modulo = models.IntegerField() 
    private_exponent = models.IntegerField() 