from rest_framework import serializers

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
        return Copy.objects.create(**validated_data)

    class Meta:
        model = Copy
        fields = ['id', 'isBorrowed', 'book_id']
        read_only_fields = ['id', 'book_id']
