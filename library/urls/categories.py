from django.urls import path

from library.views.categories import (
    CategoryRetrieveUpdateDestroyGenericView,
    CategoryListCreateGenericView
)

urlpatterns = [
    path('', CategoryListCreateGenericView.as_view()),
    path('<str:name>/', CategoryRetrieveUpdateDestroyGenericView.as_view()),
]
