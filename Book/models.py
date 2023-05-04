from django.db import models
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    author = models.CharField(max_length=50, null=False, unique=False)


class Copy(models.Model):
    isBorrowed = models.BooleanField(default=False)
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="book_copy")
