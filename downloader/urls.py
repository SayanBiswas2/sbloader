from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
  path('', views.home),
    path('youtube/',views.ythome,name='ythome'),
    path('instagram/',views.instagram,name="insta"),
    path('terms/',views.terms,name="terms"),
    path('download/',views.download,name="download"),
    path('getapp/', views.app,name="application")
]
