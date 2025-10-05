from typing import Any 
from django.db.models.query import QuerySet 
from django.shortcuts import get_object_or_404, render 
from django.http import HttpResponse, HttpResponseRedirect 
from django.urls import reverse_lazy 
from django.views import generic 
from accounts.models import message, chat, participant 
from django.conf import settings 
from users.forms import * 
import logging 
from .forms import * 
from django.forms import ModelForm 
from django.utils import timezone 
from django.contrib.auth.models import User 
from django.db.models import Q # new 
from functions import * 
from users.models import key 
from django.core.exceptions import ValidationError 
from django.contrib import messages 
 
logger = logging.getLogger() 
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User') 
 
 
class LeaveView(generic.FormView): 
    #leave chat confirmation 
    template_name = "chats/leaveChat.html" 
    form_class = RemoveChatButton 
    success_url = "/accounts/chatIndex/" 
    text = '' 
 
    def form_valid(self,form): 
        obj = participant.objects.filter(chatID = self.kwargs['pk'],userID = self.request.user) 
        obj.delete() 
        return super().form_valid(form) 
 
 
class IndexView(generic.ListView):#chat list 
    template_name = "chats/chatIndex.html" 
    context_object_name = "chat_list" 
     

    def get_queryset(self):  
        current_user = self.request.user 
        metadata =  participant.objects.filter(userID = current_user)#obtains all appropriate chats 
        chats = [] 
        for i in metadata: 
            chats.append(i.chatID) 
         
        return chats#returns list of the chat ids 
     
 
class NewChat(generic.ListView): 
    template_name = "chats/NewChat.html" 
 
    def get_queryset(self):  
        metadata =  { 
            'name': '', 
            'members': [] 
        } 
         
        return metadata 
     
    def post(self, request, *args, **kwargs): 
        forms = { 
            "name": NameForm(request.POST) 
            #"members":  
        } 
 
        form = forms["name"] 
 
        if form.is_valid():#creates chat with name from the name form 
            name = form.cleaned_data['name'] 
            current_chat = chat.objects.create(name = name) 
            participant.objects.create(userID = self.request.user, chatID = current_chat) 
            return HttpResponseRedirect(str(current_chat.chatID)+"/addUser")#redirects to the add user URL 
 
        return render(request, self.template_name,  {"name": forms["name"]}) 
 
 
class addUser(generic.ListView): 
    template_name = 'chats/addUser.html' 
    meta = {} 
 
    def get_queryset(self):  
        query = self.request.GET.get("q")#search results 
        user_to_add = CustomUser.objects.filter(username=query).first() 
        return user_to_add 
     
    def get_context_data(self, **kwargs): #obtains the primary key from the kwargs and returns query set 
        context = self.kwargs['pk'] 
        return {"i": self.get_queryset(), "pk" :context} 
     
    def post(self,request, *args, **kwargs):#adds user when button is pressed 
        form = AddUserButton(request.POST) 
 
        if form.is_valid(): 
            chatInstance = chat.objects.filter(chatID = self.kwargs['pk']).first() 
            userInstance = self.get_queryset() 
            print(userInstance) 
            participant.objects.create(userID = userInstance, chatID = chatInstance) 
            return HttpResponseRedirect(request.path) 
         
        return render(request, self.template_name,self.get_context_data()) 
 
 
 
class ChatView(generic.ListView):  
    model = chat 
    template_name = "chats/chatPage.html" 
    context_object_name = "message_list" 
    form_class = MessageForm 
 
    def create_message(self,content): 
        recipient_list = list(participant.objects.filter(chatID = self.kwargs['pk'])) 
        for i in recipient_list: #creates an encrypted message instance for each user in the chat 
            keys = [65537, key.objects.filter(uuid = i.userID)[0].modulo] 
            new_content = list_to_str(encrypt(keys,content)) 
            new_message = message(chatID= chat.objects.filter(chatID = self.kwargs['pk']).first(),  
                                senderID = self.request.user,  
                                content= new_content,  
                                recipientID = i.userID, 
                                timestamp = timezone.now()) 
            new_message.save() 
 
    def post(self, request, *args, **kwargs): #send message form 
        form = MessageForm(request.POST) 
 
        if form.is_valid(): 
            message_content = str(form.cleaned_data['new_message']) 
            self.create_message(message_content) 
            return HttpResponseRedirect(request.path, js_script) 
 
        return render(request, self.template_name,  {'message_list': self.get_queryset(), 'form': form}) 
         
    def get_queryset(self): 
        m1 = message.objects.filter(chatID = self.kwargs['pk'], recipientID = self.request.user)#obtains all appropriate messages 
        m = [] 
 
        for i in m1:#decrypts them and adds to list m 
            a = str_to_list(i.content) 
            keys = [key.objects.filter(uuid = self.request.user)[0].private_exponent, key.objects.filter(uuid = self.request.user)[0].modulo] 
            a = decrypt(keys,a) 
            a2 = { 
                "timestamp": i.timestamp, 
                "user": i.senderID.username, 
                "content": a 
            } 
  
 
            m.append(a2) 
 
        return m 
     
 
class SettingsView(generic.FormView): 
    template_name = "chats/settings.html" 
    form_class = SettingsForm 
    success_url = "/" 
    text = '' 
     
    def form_valid(self, form): 
        request = self.request 
        data = form.cleaned_data 
        if data["email"] == request.user.email or CustomUser.objects.filter(email = data["email"]).exists() == False: #checks if email is used by another user 
            user = CustomUser.objects.filter(email = request.user.email)[0] 
            user.email = data["email"] 
            user.username = data["username"] 
            user.set_password(data["password"]) 
            user.save() 
            return super().form_valid(form) 
        else: #reloads page if email is already in use by another user 
            context = {"error": True, "form": self.form_class} 
            return render(request,self.template_name,context)



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse_lazy('home'))
