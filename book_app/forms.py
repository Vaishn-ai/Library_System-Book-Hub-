from django import forms
from .models import Book, Chapter, Page


class Bookform(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'publication_year', 'isbn',
                  'copies_available', 'cover_image', 'description', 'price', 'is_free']
        widgets = {
            'genres': forms.CheckboxSelectMultiple(),
        }


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'chapter_number']


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['page_number', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }