from django.urls import path
from . import views


app_name= "Extractor" 

urlpatterns = [ 
    path('', views.index, name='index'),
    path('Extractor/login/', views.login_view, name='login_view'),
    path('Extractor/extractor_view', views.subir_pdf_view, name='extractor_view'),
]