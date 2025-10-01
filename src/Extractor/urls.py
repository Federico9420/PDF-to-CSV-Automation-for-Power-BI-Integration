from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "Extractor"

urlpatterns = [
    path('', views.index, name='index'),
    path('Extractor/login/', views.login_view, name='login_view'),
    path('Extractor/logout/', views.logout_view, name='logout_view'),
    path('Extractor/extractor_view', views.extractor_view, name='extractor_view'),
    path('Extractor/galeria/', views.galeria_view, name='galeria_view'),
    path('api/processed/', views.processed_list, name='processed_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)