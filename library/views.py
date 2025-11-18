from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from library.models import Book
from library.serializers import (
    BookListSerializer,
    BookDetailedSerializer,
    BookCreateSerializer,
    BookUpdateSerializer
)


@api_view(['GET'])
def get_all_books(request: Request) -> Response:
    # Чтобы получить список объектов, нужно эти объекты как-то достать.
    # Для этого мы обращаемся к базе и просим: "Дай все книги, что у тебя есть".
    books = Book.objects.all()

    # Сырые объекты базы — тяжелые и неповоротливые.
    # Вернуть их клиенту мы не можем. Поэтому попросим сериализатор
    # аккуратно превратить каждую книгу в обычный словарик.
    books_dto = BookListSerializer(books, many=True)

    # Теперь у нас есть простой список данных — можно смело отправлять клиенту.
    return Response(
        data=books_dto.data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_book_by_id(request: Request, book_id: int) -> Response:
    try:
        # Здесь мы пытаемся найти книгу по её номеру.
        # Если книги нет — база честно скажет: "Такой не существует"(це будет ошибка DoesNotExists).
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        # В этом случае мы сообщим клиенту, что искать дальше бессмысленно.
        return Response(
            data={"error": f"Книга с id={book_id} не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Одну книгу тоже нужно “упростить”, прежде чем отдавать её наружу.
    book_dto = BookDetailedSerializer(book)

    # И только теперь отправляем читателю простой и чистый словарь.
    return Response(
        data=book_dto.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def create_new_book(request: Request) -> Response:
    # Новая книга приходит в виде набора данных.
    # Сериализатор проверяет: всё ли заполнено, всё ли выглядит правдиво.
    book_dto = BookCreateSerializer(data=request.data)

    # Сначала убеждаемся, что данные не вызывают вопросов.
    if not book_dto.is_valid():
        # Если что-то не так, сразу честно говорим об этом клиенту.
        return Response(
            data=book_dto.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Если всё хорошо — сохраняем книгу в базу.
        # В этот момент она становится "настоящей", живущей в таблице.
        book_dto.save()
    except Exception as exc:
        # Но если база вдруг перехватит нас за рукав, мы сообщим о проблеме.
        return Response(
            data={"error": f"Ошибка при сохранении книги: {str(exc)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # В противном случае всё гуд и мы, наконец, говорим — книга создана.
    return Response(
        data=book_dto.data,
        status=status.HTTP_201_CREATED
    )


@api_view(['PUT', 'PATCH'])
def update_book(request: Request, book_id: int) -> Response:
    # PUT — это "переписать всё заново".
    # PATCH — "подправить чуть-чуть".
    partial = False if request.method == 'PUT' else True

    try:
        # Для начала найдём ту самую книгу, которую хотим поменять.
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        # Если её нет — не получится обновить то, чего нет.
        return Response(
            data={"error": f"Книга с id={book_id} не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Передаём и старый объект, и новые данные сериализатору,
    # который аккуратно обновит всё, что нужно. А так же говорим, что обновление будет, возможно, частичным (partial = True \ False)
    book_dto = BookUpdateSerializer(instance=book, data=request.data, partial=partial)

    # Проверяем, что клиент не прислал что-то странное или неуместное.
    if not book_dto.is_valid():
        return Response(
            data=book_dto.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Если всё хорошо — сохраняем изменения в базе.
        book_dto.save()
    except Exception as exc:
        # Иногда база может быть против — тогда об этом стоит сообщить.
        return Response(
            data={"error": f"Ошибка при обновлении книги: {str(exc)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Возвращаем обновлённую книгу обратно клиенту.
    return Response(
        data=book_dto.data,
        status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
def delete_book(request: Request, book_id: int) -> Response:
    try:
        # Чтобы удалить книгу, её сначала нужно найти.
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        # Если книги нет, говорим от этом клиенту
        return Response(
            data={"error": f"Книга с id={book_id} не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        # Если книга найдена — спокойно удаляем её из базы.
        book.delete()
    except Exception as exc:
        # Но база иногда может возмутиться (например, из-за связей).
        return Response(
            data={"error": f"Ошибка при удалении книги: {str(exc)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # 204 — это “всё прошло успешно, но возвращать нам нечего”.
    return Response(
        data={},
        status=status.HTTP_204_NO_CONTENT
    )
