from rest_framework.pagination import CursorPagination, PageNumberPagination

class OverrideCursorPaginator(CursorPagination):
    ordering = 'id'
    page_size = 5
