from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Chapter, Page
from .forms import Bookform, ChapterForm, PageForm
from store_app.models import Order
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from functools import wraps


def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login first.")
            return redirect('login_url')
        if not request.user.is_staff:
            messages.error(request, "Only admin can perform this action.")
            return redirect('show_book_url')
        return view_func(request, *args, **kwargs)
    return wrapper

def home_view(request):
    return render(request, 'book/home.html')


def about(request):
    return render(request, 'book/about.html')


def contact(request):
    return render(request, 'book/contact.html')


def categories(request):
    return render(request, 'book/categories.html')


# ---------------- BOOK CRUD ----------------

def create_book(request):
    form = Bookform()
    if request.method == 'POST':
        form = Bookform(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user  # assign owner
            book.save()
            form.save_m2m()  # save genres (ManyToMany)
            return redirect('show_book_url')
    return render(request, 'book/form.html', {'form': form})


def show_book(request):
    books = Book.objects.all()

    author = request.GET.get("author", "")
    genre = request.GET.get("genre", "")
    year_from = request.GET.get("year_from", "")
    year_to = request.GET.get("year_to", "")
    sort = request.GET.get("sort", "")

    if author:
        books = books.filter(author__icontains=author)
    if genre:
        books = books.filter(genres__name__icontains=genre).distinct()
    if year_from:
        books = books.filter(publication_year__gte=year_from)
    if year_to:
        books = books.filter(publication_year__lte=year_to)

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
        "books": books, "author": author, "genre": genre,
        "year_from": year_from, "year_to": year_to, "sort": sort,
    }
    return render(request, "book/show.html", context)


def categories(request):
    from .models import Genre
    categories = Genre.objects.all()
    return render(request, 'book/categories.html', {'categories': categories})


def info_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    chapters = book.chapters.all()
    return render(request, 'book/info.html', {'book': book, 'chapters': chapters})

def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not request.user.is_staff and book.owner != request.user:
        messages.error(request, "You can only edit your own books.")
        return redirect('show_book_url')
    form = Bookform(instance=book)
    if request.method == 'POST':
        form = Bookform(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('show_book_url')
    return render(request, 'book/form.html', {'form': form})


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not request.user.is_staff and book.owner != request.user:
        messages.error(request, "You can only delete your own books.")
        return redirect('show_book_url')
    book.delete()
    return redirect('show_book_url')


# ---------------- CHAPTER CRUD ----------------

def create_chapter(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    form = ChapterForm()
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.book = book
            chapter.save()
            messages.success(request, f'Chapter "{chapter.title}" added!')
            return redirect('info_book_url', pk=book.pk)
    return render(request, 'book/chapter_form.html', {'form': form, 'book': book})

@admin_only
def update_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    form = ChapterForm(instance=chapter)
    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            return redirect('info_book_url', pk=chapter.book.pk)
    return render(request, 'book/chapter_form.html', {'form': form, 'book': chapter.book})

@admin_only
def delete_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    book_pk = chapter.book.pk
    chapter.delete()
    return redirect('info_book_url', pk=book_pk)


def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    pages = chapter.pages.all()
    return render(request, 'book/chapter_detail.html', {'chapter': chapter, 'pages': pages})


# ---------------- PAGE CRUD ----------------

def create_page(request, chapter_pk):
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.chapter = chapter
            page.save()
            messages.success(request, f'Page {page.page_number} added!')
            return redirect('chapter_detail_url', pk=chapter.pk)
    return render(request, 'book/page_form.html', {'form': form, 'chapter': chapter})

@admin_only
def update_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    form = PageForm(instance=page)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('chapter_detail_url', pk=page.chapter.pk)
    return render(request, 'book/page_form.html', {'form': form, 'chapter': page.chapter})

@admin_only
def delete_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    chapter_pk = page.chapter.pk
    page.delete()
    return redirect('chapter_detail_url', pk=chapter_pk)


# ---------------- READER VIEW ----------------

@login_required(login_url='login_url')
def read_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    chapter = page.chapter
    book = chapter.book

    can_read = book.is_free or Order.objects.filter(
        user=request.user, book=book, status='completed'
    ).exists()

    if not can_read:
        messages.error(request, "You need to purchase this book to read it.")
        return redirect('book_detail', pk=book.pk)

    next_page = Page.objects.filter(chapter=chapter, page_number__gt=page.page_number).order_by('page_number').first()
    prev_page = Page.objects.filter(chapter=chapter, page_number__lt=page.page_number).order_by('-page_number').first()

    next_chapter_first_page = None
    if not next_page:
        next_chapter = Chapter.objects.filter(book=book, chapter_number__gt=chapter.chapter_number).order_by('chapter_number').first()
        if next_chapter:
            next_chapter_first_page = next_chapter.pages.order_by('page_number').first()

    context = {
        'page': page, 'chapter': chapter, 'book': book,
        'next_page': next_page, 'prev_page': prev_page,
        'next_chapter_first_page': next_chapter_first_page,
    }
    return render(request, 'book/read_page.html', context)