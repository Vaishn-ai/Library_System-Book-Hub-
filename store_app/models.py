from django.db import models
from django.contrib.auth.models import User
from book_app.models import Book
import uuid


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Order(models.Model):
    STATUS = [
        ('pending', 'Pending Payment'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    ordered_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = "BH" + uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.user.username} - {self.book.title}"


class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    last_read = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} reading {self.book.title}"