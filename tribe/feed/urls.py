from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.create_post,name='create_post'),
   path('comment/add/', views.add_comment, name='add_comment'),
   path('like/toggle/', views.toggle_like, name='toggle_like'),
   
]
