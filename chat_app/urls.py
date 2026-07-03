from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_view, name='chat_url'),
    path('chat/api/', views.chat_api, name='chat_api_url'),
    path('chat/clear/', views.clear_chat, name='chat_clear_url'),
]