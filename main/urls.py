from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('success/<str:filename>/', views.download_file, name='download_file'),
]
