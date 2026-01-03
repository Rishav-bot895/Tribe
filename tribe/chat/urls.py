from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_chat, name='create_chat'),
    path('<str:group_name>/leave/', views.leave_chat, name='leave_chat'),
    path('<str:group_name>/add/', views.add_users, name='add_users'),
    path('', views.chat_list, name='chat_list'),
    path('<str:group_name>/', views.chat_room, name='chat_room'),
]

