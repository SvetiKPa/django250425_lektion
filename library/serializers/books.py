from rest_framework import serializers

from library.models import Book


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'price',
            'publication_date'
        ]


class BookDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'title',
            'description',
            'category',
            'page_count',
            'publisher',
            'category',
            'author',
            'price'
        )


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'title',
            'description',
            'category',
            'page_count',
            'publisher',
            'category',
            'author',
            'price'
        )
