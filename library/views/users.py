from datetime import datetime

from django.contrib.auth import authenticate
from django.db.models.aggregates import Count
from django.utils.timezone import make_aware
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from library.models import User
from library.serializers import UserListSerializer, UserCreateSerializer
from library.utils import set_jwt_cookies


class UserListCreateGenericView(ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context['include_related'] = self.request.query_params.get(
            'include_related', 'false'
        ).lower() == 'true'

        return context

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer

        return UserCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = User.objects.annotate(
            posts_cnt=Count('posts')
        ).filter(posts_cnt__gt=0)

        serializer = self.get_serializer(queryset, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

# class UserListCreateGenericView(GenericAPIView):
#     queryset = User.objects.all()
#     # serializer_class = UserListSerializer
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return UserListSerializer
#
#         return UserCreateSerializer
#
#     def get(self, request: Request, *args, **kwargs) -> Response:
#         users = self.get_queryset()
#
#         if not users:
#             return Response(
#                 data=[],
#                 status=status.HTTP_204_NO_CONTENT
#             )
#
#         serializer = self.get_serializer(users, many=True)  # -> UserListSerializer(...)
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )
#
#     def post(self, request: Request, *args, **kwargs) -> Response:
#         serializer = self.get_serializer(data=request.data)
#
#         if not serializer.is_valid():
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         serializer.save()
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_201_CREATED
#         )


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request):
        qs = User.objects.all()
        serializer = UserListSerializer(qs, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


    def post(self, request: Request) -> Response:
        serializer = UserCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()

        response = Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

        set_jwt_cookies(response, user)

        return response


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = authenticate(
                request=request,
                username=username,
                password=password
            )

            if user:
                response = Response(status=status.HTTP_200_OK)

                set_jwt_cookies(response, user)

                return response
            else:
                return Response(
                    data={
                        "message": "Invalid username or password"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as exc:
            return Response(
                data={
                    "message": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogOutUser(APIView):
    def post(self, request: Request) -> Response:
        try:
            refresh = request.COOKIES.get('refresh_token')

            if refresh:
                token = RefreshToken(refresh)
                token.blacklist()

        except Exception as exc:
            return Response(
                data={
                    "message": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
