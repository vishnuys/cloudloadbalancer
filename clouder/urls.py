"""clouder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from loader import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.DefaultView.as_view()),
    path('status/', views.StatusChecker.as_view()),
    path('create/bucket/', views.CreateBucket.as_view()),
    path('delete/bucket/', views.DeleteBucket.as_view()),
    path('create/file/', views.CreateFile.as_view()),
    path('delete/file/', views.DeleteFile.as_view()),
    path('update/file/', views.UpdateFile.as_view()),
    path('read/file/', views.ReadFile.as_view()),
    path('file/<name>', views.FileDownload.as_view()),
    path('gossip/',views.RecieveGossip.as_view())
]
