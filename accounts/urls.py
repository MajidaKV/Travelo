from . import views
from django.urls import path

urlpatterns = [
    
    path('register', views.register,name='register'), 
    path('verification',views.verification, name='verification')
    path('login', views.loginView,name='login'),    
]