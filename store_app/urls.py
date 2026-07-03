from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store_home, name='store_home'),
    path('store/book/<int:pk>/', views.book_detail, name='book_detail'),
    path('store/cart/', views.view_cart, name='view_cart'),
    path('store/cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('store/cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('store/buy/<int:pk>/', views.buy_book, name='buy_book'),
    path('store/payment/confirm/<str:order_id>/', views.confirm_payment, name='confirm_payment'),
    path('store/payment/receipt/<str:order_id>/', views.payment_receipt, name='payment_receipt'),
    path('store/orders/', views.my_orders, name='my_orders'),
]