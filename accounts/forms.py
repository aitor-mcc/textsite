from typing import Any 
from django import forms 
from django.core.exceptions import ValidationError 
 
class MessageForm(forms.Form): 
    new_message = forms.CharField(label="new message:", max_length=1000) 

  
 
class NameForm(forms.Form): 
    name = forms.CharField(label="username:", max_length=100) 
 
class UsersForm(forms.Form): 
    name = forms.CharField(label="Find User:", max_length=100) 
 
class AddUserButton(forms.Form): 
   button = forms.NullBooleanField() 
 
class SettingsForm(forms.Form): 
    username = forms.CharField(label = "username:", max_length= 100) 
    email = forms.EmailField(label = "email:") 
    password = forms.CharField(label = "new password:") 
 
class RemoveChatButton(forms.Form): 
   button = forms.NullBooleanField()