from django.db import models
from django.db import models


class Book(models.Model):
    class Meta:
        ordering = ("id",)
    name = models.CharField(max_length=50, null=False, unique=True)
    # following = models.ManyToManyField(
    #     'User.User', related_name='followed_books')
    author = models.CharField(max_length=50, null=False, unique=False)


class Copy(models.Model):
    isBorrowed = models.BooleanField(default=False)
    book = models.ForeignKey(
        "Book.Book", on_delete=models.CASCADE, related_name="book_copy")
