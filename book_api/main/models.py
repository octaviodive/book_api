from django.db import models
from user.models import CustomUser
# Create your models here.
class Book(models.Model):
    id_book = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=150, blank=False)
    publication_date = models.PositiveIntegerField(blank=False)

    def __str__(self) -> str:
        return str(self.id_book)

class Comment(models.Model):
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'ID: {self.book}, Created: {self.created_date}'

        


