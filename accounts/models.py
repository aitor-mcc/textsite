from django.db import models 
from django.utils import timezone 
from django.contrib import admin 
from django.conf import settings 
from django.apps import apps 
from django.contrib.auth import get_user_model 
from django.core.signals import setting_changed 
from django.dispatch import receiver 
import datetime 
 
#settings.AUTH_USER_MODEL when referencing users 
class chat(models.Model): 
    chatID = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=50) 
     
    def __str__(self): 
        return self.name 
 
     
class message(models.Model): 
    messageID = models.AutoField(primary_key=True) 
    chatID = models.ForeignKey(chat, on_delete=models.CASCADE) 
    senderID = models.ForeignKey(get_user_model(),related_name= "sender", on_delete=models.CASCADE) 
    recipientID = models.ForeignKey(get_user_model(),related_name = "recipient", on_delete=models.CASCADE) 
    content = models.CharField(max_length=1000) 
    timestamp = models.DateTimeField("date published") 

 
class participant(models.Model): 
    participantID = models.AutoField(primary_key= True) 
    chatID = models.ForeignKey(chat, on_delete=models.CASCADE) 
    userID = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)