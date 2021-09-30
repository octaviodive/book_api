from django.contrib import admin
from main.models import Book, Comment
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    fields = [
        'id_book',
        'title',
        'publication_date'
    ]

class CommentAdmin(admin.ModelAdmin):
    fields = [
        'text',
        'book',
        'user'
    ]
admin.site.register(Book, BookAdmin)
admin.site.register(Comment, CommentAdmin)


