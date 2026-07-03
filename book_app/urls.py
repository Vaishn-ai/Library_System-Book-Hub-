from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home_url'),
    path('about/', about, name='about_url'),
    path('contact/', contact, name='contact_url'),
    path('categories/', categories, name='categories_url'),

    # Book
    path('create/', create_book, name='create_book_url'),
    path('show/', show_book, name='show_book_url'),
    path('info/<int:pk>/', info_book, name='info_book_url'),
    path('update/<int:pk>/', update_book, name='update_book_url'),
    path('delete/<int:pk>/', delete_book, name='delete_book_url'),

    # Chapter
    path('book/<int:book_pk>/chapter/create/', create_chapter, name='create_chapter_url'),
    path('chapter/<int:pk>/', chapter_detail, name='chapter_detail_url'),
    path('chapter/<int:pk>/update/', update_chapter, name='update_chapter_url'),
    path('chapter/<int:pk>/delete/', delete_chapter, name='delete_chapter_url'),

    # Page
    path('chapter/<int:chapter_pk>/page/create/', create_page, name='create_page_url'),
    path('page/<int:pk>/update/', update_page, name='update_page_url'),
    path('page/<int:pk>/delete/', delete_page, name='delete_page_url'),
    path('page/<int:pk>/read/', read_page, name='read_page_url'),
]