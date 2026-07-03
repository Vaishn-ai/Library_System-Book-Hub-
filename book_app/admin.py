from django.contrib import admin
from .models import Book, Chapter, Page, ContactMessage, Genre


class PageInline(admin.TabularInline):
    model = Page
    extra = 1


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('book', 'chapter_number', 'title', 'total_pages')
    inlines = [PageInline]


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'price', 'is_free', 'total_chapters')
    filter_horizontal = ('genres',)
    inlines = [ChapterInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Page)
admin.site.register(ContactMessage)