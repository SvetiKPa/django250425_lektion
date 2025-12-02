from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from library.views.publishers import PublisherViewSet


router = SimpleRouter()
# router = DefaultRouter()
router.register('publisher', PublisherViewSet)  # /api/v1/publishers/
                                                      # /api/v1/publishers/<pk>


urlpatterns = [
    path('books/', include('library.urls.books')),
    path('users/', include('library.urls.users')),
    path('categories/', include('library.urls.categories')),
    path('token-auth/', obtain_auth_token),
    path('jwt-auth/', TokenObtainPairView.as_view()),
    path('jwt-refresh/', TokenRefreshView.as_view()),
] + router.urls
