from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_book, name='create_book_url'),
    path('show/', show_book, name='show_book_url'),
    path('show2/', show2_book, name='show2_book_url'),
    path('info/<int:pk>/', info_book, name='info_book_url'),
    path('update/<int:pk>/', update_book, name='update_book_url'),
    path('delete/<int:pk>/', delete_book, name='delete_book_url'),
    path('', home_view, name='home_url'),
    path('about/', about, name='about_url'),
    path('contact/', contact, name='contact_url'),
    path('categories/', categories, name='categories_url'),
]
