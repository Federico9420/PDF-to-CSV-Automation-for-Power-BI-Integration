from django.urls import path
from . import views

urlspatterns = [ 
    path('', views.index, name='index.html'),
    path('Login', views.login, name= 'login.html')

]