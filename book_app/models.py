from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='books')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre, related_name='books')  # replaces old `genre` CharField
    publication_year = models.IntegerField()
    isbn = models.CharField(max_length=20, unique=True)
    copies_available = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

    @property
    def total_chapters(self):
        return self.chapters.count()


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    chapter_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chapter_number']
        unique_together = ('book', 'chapter_number')

    def __str__(self):
        return f"{self.book.title} - Ch {self.chapter_number}: {self.title}"

    @property
    def total_pages(self):
        return self.pages.count()


class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')
    page_number = models.PositiveIntegerField()
    content = models.TextField()

    class Meta:
        ordering = ['page_number']
        unique_together = ('chapter', 'page_number')

    def __str__(self):
        return f"{self.chapter.book.title} - Ch {self.chapter.chapter_number} - Pg {self.page_number}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name