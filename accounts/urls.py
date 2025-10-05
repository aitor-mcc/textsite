from django.urls import path 
from .views import ChatView, IndexView, NewChat, addUser, SettingsView, LeaveView 
from . import views 
 
app_name = "accounts" 
urlpatterns = [ 
    path("<int:pk>/leave", LeaveView.as_view(), name = "leave"), 
    path("settings", SettingsView.as_view(), name="settings"), 
    path("<int:pk>/messages/", ChatView.as_view(), name="messages"), 
    path("chatIndex/",IndexView.as_view(),name="chat index"), 
    path("newChat/",NewChat.as_view(),name="new chat"), 
    path("newChat/<int:pk>/addUser",addUser.as_view(),name="add user"),
    path("logout/", views.logout_view, name="logout")
] 