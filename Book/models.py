from django.db import models
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)


class Copy(models.Model):
    isBorrowed = models.BooleanField(default=False)
    book = models.ForeignKey(
        "Book.Book", on_delete=models.CASCADE, related_name="book_copy")
