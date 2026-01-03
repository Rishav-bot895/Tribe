from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.account_details,name='account_details'),
   
]