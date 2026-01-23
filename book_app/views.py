from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import Bookform

# Create your views here.

def home_view(request):
    template_name = 'book/home.html'
    return render(request, template_name)

def about(request):
    template_name = 'book/about.html'
    return render(request, template_name)

def contact(request):
    template_name = 'book/contact.html'
    return render(request, template_name)

def categories(request):
    template_name = 'book/categories.html'
    return render(request, template_name)


def create_book(request):
    form = Bookform()
    if request.method == 'POST':
        form = Bookform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_book_url')
        else:
            print(form.errors)
    template_name = 'book/form.html'
    context = {'form': form}
    return render(request, template_name, context)


def show_book(request):
    books = Book.objects.all()
    
    author = request.GET.get("author", "")
    genre = request.GET.get("genre", "")
    year_from = request.GET.get("year_from", "")
    year_to = request.GET.get("year_to", "")

    if author:
        books = books.filter(author__icontains=author)

    if genre:
        books = books.filter(genre__icontains=genre)

    if year_from:
        books = books.filter(publication_year__gte=year_from)

    if year_to:
        books = books.filter(publication_year__lte=year_to)
\
    sort = request.GET.get("sort", "")

    if sort == "title_asc":
        books = books.order_by("title")
    elif sort == "title_desc":
        books = books.order_by("-title")
    elif sort == "year_new":
        books = books.order_by("-publication_year")
    elif sort == "year_old":
        books = books.order_by("publication_year")
    elif sort == "copies_high":
        books = books.order_by("-copies_available")
    elif sort == "copies_low":
        books = books.order_by("copies_available")

    context = {
        "books": books,
        "author": author,
        "genre": genre,
        "year_from": year_from,
        "year_to": year_to,
        "sort": sort,   
    }

    return render(request, "book/show.html", context)


def show2_book(request):
    books = Book.objects.all()
    
    author = request.GET.get("author", "")
    genre = request.GET.get("genre", "")
    year_from = request.GET.get("year_from", "")
    year_to = request.GET.get("year_to", "")

    if author:
        books = books.filter(author__icontains=author)

    if genre:
        books = books.filter(genre__icontains=genre)

    if year_from:
        books = books.filter(publication_year__gte=year_from)

    if year_to:
        books = books.filter(publication_year__lte=year_to)
\
    sort = request.GET.get("sort", "")

    if sort == "title_asc":
        books = books.order_by("title")
    elif sort == "title_desc":
        books = books.order_by("-title")
    elif sort == "year_new":
        books = books.order_by("-publication_year")
    elif sort == "year_old":
        books = books.order_by("publication_year")
    elif sort == "copies_high":
        books = books.order_by("-copies_available")
    elif sort == "copies_low":
        books = books.order_by("copies_available")

    context = {
        "books": books,
        "author": author,
        "genre": genre,
        "year_from": year_from,
        "year_to": year_to,
        "sort": sort,   
    }

    return render(request, "book/show2.html", context)


def info_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    template_name = 'book/info.html'
    context = {'book': book}
    return render(request, template_name, context)

def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = Bookform(instance=book)
    if request.method=='POST':
        form = Bookform(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('show_book_url')
    context = {'form' : form}
    template_name = 'book/form.html'
    return render(request, template_name, context)

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('show_book_url')