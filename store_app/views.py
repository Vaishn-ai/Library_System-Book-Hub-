from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from book_app.models import Book
from .models import Cart, Order
from book_app.models import Book, Genre
import qrcode
import io
import base64
import urllib.parse


def store_home(request):
    books = Book.objects.all()
    categories = Genre.objects.all()  # import Genre from book_app.models
    selected_cat = request.GET.get('category', '')
    if selected_cat:
        books = books.filter(genres__name=selected_cat).distinct()
    return render(request, 'store/store_home.html', {
        'books': books, 'categories': categories, 'selected_cat': selected_cat,
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    already_ordered = False
    in_cart = False
    if request.user.is_authenticated:
        already_ordered = Order.objects.filter(user=request.user, book=book, status='completed').exists()
        in_cart = Cart.objects.filter(user=request.user, book=book).exists()
    return render(request, 'store/book_detail.html', {
        'book': book, 'already_ordered': already_ordered, 'in_cart': in_cart,
    })


@login_required(login_url='login_url')
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if created:
        messages.success(request, f'"{book.title}" added to cart!')
    else:
        messages.info(request, f'"{book.title}" is already in your cart.')
    return redirect('view_cart')


@login_required(login_url='login_url')
def remove_from_cart(request, pk):
    Cart.objects.filter(user=request.user, book__pk=pk).delete()
    messages.success(request, "Book removed from cart.")
    return redirect('view_cart')


@login_required(login_url='login_url')
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.book.price for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


# ---------------- PAYMENT FLOW ----------------

UPI_ID = "yourname@upi"  # replace with your actual UPI ID
PAYEE_NAME = "BookHub"


@login_required(login_url='login_url')
def buy_book(request, pk):
    """Step 1: create a pending order and show QR code for payment."""
    book = get_object_or_404(Book, pk=pk)

    if Order.objects.filter(user=request.user, book=book, status='completed').exists():
        messages.info(request, "You already own this book.")
        return redirect('book_detail', pk=pk)

    order, created = Order.objects.get_or_create(
        user=request.user, book=book, status='pending',
        defaults={'amount': book.price}
    )

    # Build UPI payment URL
    upi_url = (
        f"upi://pay?pa={UPI_ID}&pn={urllib.parse.quote(PAYEE_NAME)}"
        f"&am={order.amount}&cu=INR&tn={urllib.parse.quote('Order ' + order.order_id)}"
    )

    qr = qrcode.make(upi_url)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    qr_base64 = base64.b64encode(buf.getvalue()).decode()

    return render(request, 'store/payment.html', {
        'book': book, 'order': order, 'qr_base64': qr_base64, 'upi_url': upi_url,
    })


@login_required(login_url='login_url')
def confirm_payment(request, order_id):
    """Step 2: user confirms they paid. In real life this would be a webhook callback."""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)

    if order.status == 'pending':
        order.status = 'completed'
        order.paid_at = timezone.now()
        order.save()
        Cart.objects.filter(user=request.user, book=order.book).delete()
        messages.success(request, "Payment confirmed! You can now read your book.")

    return redirect('payment_receipt', order_id=order.order_id)


@login_required(login_url='login_url')
def payment_receipt(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'store/receipt.html', {'order': order})


@login_required(login_url='login_url')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'store/my_orders.html', {'orders': orders})