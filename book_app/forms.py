from django import forms
from .models import Book
from django.core import validators


class Bookform(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']

        if len(isbn) not in [10,13]:
            raise validators.ValidationError('Isbn must be 10 or 13 digit.')

        if not isbn.isdigit():
            raise validators.ValidationError('Isbn should contain only numbers.')

        return isbn

    def clean_publication_year(self):
        year = self.cleaned_data['publication_year']

        if year < 1500 or year > 2100:
            raise validators.ValidationError('Publication year must be between 1500 and 2100.')
        return year

    def clean_copies_available(self):
        copies = self.cleaned_data['copies_available']

        if copies <0:
            raise validators.ValidationError('Copies cannot be negative')
        return copies

        


    

    