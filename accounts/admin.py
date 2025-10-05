from django.contrib import admin 
from django.contrib import admin 
from .models import chat, message, participant 
 
class messageInline(admin.TabularInline): 
    model = message 
    extra = 1 
 
class participantInline(admin.TabularInline): 
    model = participant 
    extra = 1 
 
 
class chatAdmin(admin.ModelAdmin): 
    model = chat 
    readonly_fields=('chatID',) 
    inlines = [messageInline,participantInline] 
 
 
admin.site.register(chat, chatAdmin) 
admin.site.register(message) 
admin.site.register(participant)