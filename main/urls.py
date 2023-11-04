from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('success/<str:filename>/', views.download_file, name='download_file'),
    path('help/', views.help_page, name='help_page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]
