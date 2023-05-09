from django.forms import model_to_dict
from rest_framework import serializers

from Book.tasks import send_notification

from .models import Book, Copy


class BookSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    class Meta:
        model = Book
        fields = ['id', 'name', 'author']
        read_only_fields = ['id']


class CopySerializer(serializers.ModelSerializer):
    def create(self, validated_data):

        book = validated_data["book"]

        for user in model_to_dict(book)["following"]:
            send_notification(user, book, "isavaliable")

        return Copy.objects.create(**validated_data)

    class Meta:
        model = Copy
        fields = ['id', 'isBorrowed', 'book']
        read_only_fields = ['id']
