from datetime import datetime

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.timezone import make_aware
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from src.authentication.dtos import (
    RegisterUserDTO,
    ListUsersDTO,
    DetailedUserDTO,
    UpdateUserDTO,
    ChangePasswordDTO
)
from src.permissions.users import IsAdminOrSelf, IsAnonymous


# Список пользователей + регистрация
class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListUsersDTO
        return RegisterUserDTO

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAnonymous()]  # регистрация доступна всем
        return [permissions.IsAdminUser()]  # список пользователей виден только админам


# Работа с конкретным пользователем
class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelf]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DetailedUserDTO
        return UpdateUserDTO

class LoginUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        login, password = request.data.get('username'), request.data.get('password')

        try:
            user = authenticate(
                request=request,
                username=login,
                password=password
            )

            if user:
                response = Response(status=status.HTTP_200_OK)


                refresh = RefreshToken.for_user(user)
                access = refresh.access_token

                refresh_exp = make_aware(
                    datetime.fromtimestamp(refresh.payload['exp'])
                )
                access_exp = make_aware(
                    datetime.fromtimestamp(access.payload['exp'])
                )

                response.set_cookie(
                    key='refresh',
                    value=str(refresh),
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    expires=refresh_exp
                )

                response.set_cookie(
                    key='access',
                    value=str(access),
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    expires=access_exp
                )

                return response

            else:
                return Response(
                    data={
                        'error': 'Invalid username or password'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return Response(
                data={
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutUserAPIView(APIView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            refresh_token = request.COOKIES.get('refresh')

            if refresh_token:
                token = RefreshToken(refresh_token)

                token.blacklist()

            response = Response(status=status.HTTP_200_OK)
        except Exception as e:
            response = Response(
                data={
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            response.delete_cookie('access')
            response.delete_cookie('refresh')
            return response

class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordDTO(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password successfully changed"}, status=status.HTTP_200_OK)
