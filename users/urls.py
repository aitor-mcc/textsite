from django.urls import path 
from .views import signup 
from . import views 
 
app_name = "users" 
urlpatterns = [ 
    path("signup/", signup, name="signup"), 
]