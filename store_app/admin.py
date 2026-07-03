from django.contrib import admin
from .models import Cart, Order, ReadingProgress

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(ReadingProgress)