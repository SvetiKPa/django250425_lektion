import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


# from rest_framework.authtoken.models import Token
# from library.models import User
#
# user = User.objects.get(username='vladislav')
#
# token, created = Token.objects.get_or_create(user=user)
#
# print(created)
# print(token.user)
# print(token.key)


# from test_app.models import (
#     Book,
#     UserProfile
# )


# try:
#     book = Book.objects.get(author="Leo Tolstoy")  # MultipleObjectsReturned
#     # book = Book.objects.get(id=999999999)  # DoesNotExist
#
#     print(book)
# except Book.DoesNotExist as err:
#     print("Нет такой книги", err)
# except Book.MultipleObjectsReturned as err:
#     print("Слишком много книг найдено", err)


# leo_books = Book.objects.filter(author="Leo Tolstoy")
#
# print(leo_books.query)
# print(leo_books)


# __contains == частичное совпадение с учётом регистра
# __icontains == частичное совпадение БЕЗ учёта регистра
# i == ignore_case

# leo_books = Book.objects.filter(title__contains="P")
#
# print(leo_books.query)
# print(leo_books)



# books = Book.objects.filter(id__in=[15, 280, 361])
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.title)


# books = Book.objects.filter(pages__gt=500)
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.title)


# filter(<field_name>__<lookups_name>)
# books = Book.objects.filter(published_date__gte="2020-01-01")
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.published_date)


# books = Book.objects.filter(pages__isnull=True)
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.published_date)


# books = Book.objects.filter(title__startswith="A")
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.published_date)


# books = Book.objects.filter(pages__range=[<start>, <stop>])
# books = Book.objects.filter(pages__range=[500, 700])
#
# print(books.query)
#
# for b in books:
#     print(f"{b.id=}  -- {b.pages=}")


#
# books = Book.objects.filter(
#     pages__range=[500, 700],
#     published_date__gte='2020-01-01'
# )
#
# print(books.query)
#
# for b in books:
#     print(f"{b.id=}  -- {b.pages=}")



# =====================================================================

# from django.db.models import Q

# Q class

# OR - |
# AND - &
# NOT - ~

# data = Book.objects.filter(
#     Q(Q(author__startswith="Fyodor") | Q(author__startswith="Jack")) & Q(published_date__gte='2015-05-31')
# )
#
# print(data.query)
#
# for b in data:  # type: Book
#     print(f"{b.id=}  --  {b.author}  --  {b.published_date}")


# """
# SELECT
#     "books"."id",
#     "books"."title",
#     "books"."description",
#     "books"."author",
#     "books"."published_date",
#     "books"."pages"
# FROM "books"
# WHERE (
#           ("books"."author" LIKE Fyodor% ESCAPE '\'
#           OR "books"."author" LIKE Jack% ESCAPE '\'
#           )
#               AND "books"."published_date" >= 2015-05-31
#       )
# ORDER BY "books"."published_date" ASC
#
# """


# data = Book.objects.filter(
#     Q(
#         Q(author__startswith="Fyodor") | Q(Q(author__startswith="Jack") & ~Q(author__endswith="London"))
#     ) & Q(published_date__gte='2015-05-31')
# )
#
# print(data.query)
#
# for b in data:  # type: Book
#     print(f"{b.id=}  --  {b.author}  --  {b.published_date}")

from decimal import Decimal

# book = Book.objects.get(id=700)
#
# print("BEFORE:")
# print(book.is_bestseller)
# print(book.price)
#
#
# book.is_bestseller = True
# book.price = Decimal("189.97")
#
# book.save()
# print("AFTER:")
# print(book.is_bestseller)
# print(book.price)


# books = Book.objects.filter(
#     author__in=["Leo Tolstoy", "Fyodor Dostoevsky"]
# ).update(is_bestseller=True, price=Decimal("299.99"))
#


# from django.db.models import F
#
#
# books = Book.objects.filter(
#     author__in=["Leo Tolstoy", "Fyodor Dostoevsky"]
# ).update(discounted_price=F('price') * 0.80)



# book_to_delete = Book.objects.get(id=720)
#
#
# book_to_delete.delete()
#
#
#
# Book.objects.create()
# Book.objects.bulk_create()
# Book.objects.bulk_update()



# =====================================================
# New Lecture AGGREGATE && ANNOTATE
# =====================================================

from library.models import Book, Category
from django.db.models import (
    Avg,
    Count,
    Min,
    Max, Subquery, OuterRef
)
from typing import Any

# Посчитать общее кол-во книг + средняя цена всех книг

# {} -> aggregate()

# aggregate_result: dict[str, Any] = Book.objects.aggregate(
#     books_count=Count('id'),
#     avg_books_price=Avg('price')
# )

# print(f"Общее кол-во всех книг в базе = ", aggregate_result['books_count'])
# print(f"Общее кол-во всех книг в базе = ", aggregate_result.get('books_count'))

# print(f"Средняя цена всех книг в базе = ", aggregate_result['avg_books_price'])
# print(f"Средняя цена всех книг в базе = ", aggregate_result.get('avg_books_price'))



# aggregate_result_min_max: dict[str, Any] = Book.objects.aggregate(
#     min_book_aprice=Min('price'),
#     max_book_price=Max('price')
# )
#
# print(aggregate_result_min_max)


# annotate()


# annotated_books_with_custom_field = Book.objects.values('author').annotate(
#     books_count=Count('id')
# ) # <QuerySet[{...}, ..., {...}]>

# print(annotated_books_with_custom_field.query)


# for obj in annotated_books_with_custom_field:
#     print(f"Автор: {obj.author}, кол-во книг = {obj.books_count}")


# for obj in annotated_books_with_custom_field:
#     print(f"Автор: {obj['author']}, кол-во книг = {obj['books_count']}")


# books_by_category = Category.objects.values('name_category').annotate(
#     books_count=Count('books')
# )

# print(books_by_category)

# for obj in books_by_category:
#     print(f"Категории: {obj['name_category']}, кол-во книг = {obj['books_count']}")
#
# from library.models import Borrow
# from django.db.models import (Count, Q)
#
# data = Borrow.objects.values('member__username').annotate(
#     count_aktiv_borrow=Count('id', filter=Q(returned=False))
# ).order_by('-count_aktiv_borrow')[:5]  # 0 -4 index
#
#
# print(data)


from library.models import Borrow, User
from django.db.models import (Count, Q)


# 2 var
# data = (
#     Borrow.objects
#     .filter(returned=False)
#     .values('member__username')
#     .annotate(borrows_cnt=Count('id'))
#     .order_by('-borrows_cnt')
# )[:5]
#
#
# for item in data:
#     print(item)
#
#
# 3 var
#
# data = (
#     User.objects
#     .values('last_name', 'first_name')
#     .annotate(
#         borrows_count=Count(
#             'borrows',
#             filter=Q(borrows__returned=False)
#         )
#     )
#     .order_by('-borrows_count')
# )[:5]


# ПОЛУЧИТЬ список книг цена которых выше срадней у того же автора

# from django.db.models import F
#
# subquery = (
#     Book.objects
#     .filter(author=OuterRef('author'))
#     .values('author')
#     .annotate(avg_price=Avg('price'))
#     .values('avg_price')
# )
#
#
# general_query = (
#     Book.objects
#     .annotate(avg_price_by_author=Subquery(subquery))
#     .filter(
#         price__gt=F('avg_price_by_author')
#     )
# )

# """
# SELECT t1.*, (
#         SELECT Avg(t2.price) as avg_price
#         FROM books AS t2
#         WHERE t2.author_id = t1.author_id
#     ) AS avg_price_by_author
# FROM books as t1
# WHERE
#     author_id = 1 AND
#     t1.price > avg_price_by_author
# ;
# """

#
# from rest_framework import serializers
# from library.models import Category
#
#
# class UserCustomSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=25)
#     age = serializers.IntegerField(min_value=15)
#     is_active = serializers.BooleanField()
#     created_at = serializers.DateTimeField()
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     # name_categoy = ...
#
#     class Meta:
#         model = Category
#         fields = "__all__"
#         # fields = ["id", "category_name"]
#
#
# raw_data = {
#     "name": "Johnny",
#     "age": 18,
#     "is_active": True,
#     "created_at": "2022-09-17T16:31:15",
# }
#
#
# data = UserCustomSerializer(data=raw_data)
#
# print(data)
#
#
# if data.is_valid():
#     print(data.validated_data)
#
# else:
#     print("ДАННЫЕ НЕВАЛИДНЫ")
#     print(data.errors)



# class Book:
#     title = "TEST"
#     price = 22.9
#     pages = 228
#
#     def __str__(self):
#         return f"{self.title=} {self.price=} {self.pages=}"
#
#
#
# validated_data = {
#     "price": 99
# }
# book = Book()
#
#
# for attr, value in validated_data.items():
#     setattr(book, attr, value)
#
#
# print(book)


# title = "TEST TITLE"
#
# print(title.replace(" ", "").isalnum())

# "$#@!_-+=*&^%><?/\|"
#
# result = all(word.isalnum() for word in title.split(' '))
#
# print(result)


# Book.objects.filter(
#     publication_date__year=1997,
#     publication_date__month=7,
#     publication_date__day=5,
# )


# http://localhost:8000/subtasks/?parent_name=CREATE%20New%20Obj&status=In%20Progres
# http://localhost:8000/subtasks/?status=In%20Progres
# http://localhost:8000/subtasks/?parent_name=CREATE%20New%20Obj
