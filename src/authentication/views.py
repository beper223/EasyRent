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
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated

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
    """
    API endpoint для работы со списком пользователей.
    - GET: возвращает список пользователей (только для администраторов)
    - POST: регистрация нового пользователя
    
    API-Endpunkt für die Benutzerverwaltung.
    - GET: Gibt eine Liste der Benutzer zurück (nur für Administratoren)
    - POST: Registriert einen neuen Benutzer
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Возвращает соответствующий сериализатор в зависимости от метода запроса.
        - GET: ListUsersDTO - список пользователей
        - POST: RegisterUserDTO - регистрация пользователя
        
        Gibt den entsprechenden Serializer basierend auf der Anfragemethode zurück.
        - GET: ListUsersDTO - Benutzerliste
        - POST: RegisterUserDTO - Benutzerregistrierung
        """
        if self.request.method == 'GET':
            return ListUsersDTO
        return RegisterUserDTO

    def get_permissions(self):
        """
        Определяет права доступа в зависимости от метода запроса.
        - POST: доступно всем (регистрация)
        - GET: только для администраторов
        
        Bestimmt die Zugriffsrechte basierend auf der Anfragemethode.
        - POST: für alle verfügbar (Registrierung)
        - GET: nur für Administratoren
        """
        if self.request.method == "POST":
            return [IsAnonymous()]  # регистрация доступна всем
        return [permissions.IsAdminUser()]  # список пользователей виден только админам

class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint для работы с конкретным пользователем.
    - GET: просмотр профиля
    - PATCH: частичное обновление
    - DELETE: деактивация пользователя
    
    API-Endpunkt für die Arbeit mit einem bestimmten Benutzer.
    - GET: Profil anzeigen
    - PATCH: Teilweise Aktualisierung
    - DELETE: Deaktivierung des Benutzers
    """
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelf]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DetailedUserDTO
        return UpdateUserDTO

    def perform_destroy(self, instance: User):
        """
        Вместо физического удаления:
        - деактивируем пользователя (is_active = False)
        - разлогиниваем его (отзываем все JWT refresh-токены)
        
        Anstatt den Benutzer physisch zu löschen:
        - Deaktiviert den Benutzer (is_active = False)
        - Meldet den Benutzer ab (widerruft alle JWT-Aktualisierungstoken)
        """
        instance.is_active = False
        instance.save()

        tokens = OutstandingToken.objects.filter(user=instance)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "User deactivated and logged out."},
            status=status.HTTP_204_NO_CONTENT,
        )

class LoginUserAPIView(APIView):
    """
    API для аутентификации пользователя.
    Принимает username и password, возвращает JWT-токены в HttpOnly куках.
    
    API zur Benutzerauthentifizierung.
    Nimmt Benutzername und Passwort entgegen und gibt JWT-Token in HttpOnly-Cookies zurück.
    
    Параметры запроса (JSON):
    - username: Имя пользователя
    - password: Пароль
    
    Anforderungsparameter (JSON):
    - username: Benutzername
    - password: Passwort
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        login, password = request.data.get('username'), request.data.get('password')

        try:
            user = authenticate(
                request=request,
                username=login,
                password=password
            )

            if not user:
                return Response({'error': 'Invalid username or password'},status=status.HTTP_401_UNAUTHORIZED)

            response = Response({"detail": "Login successful"},status=status.HTTP_200_OK)

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

        except Exception as e:
            return Response(
                data={
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutUserAPIView(APIView):
    """
    API для выхода пользователя из системы.
    Отзывает refresh-токен и удаляет куки аутентификации.
    
    API zum Abmelden des Benutzers.
    Widerruft das Aktualisierungstoken und entfernt die Authentifizierungs-Cookies.
    """

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
    """
    API для изменения пароля пользователя.
    Требует аутентификации.
    
    API zum Ändern des Benutzerpassworts.
    Erfordert Authentifizierung.
    
    Параметры запроса (JSON):
    - old_password: Текущий пароль
    - new_password: Новый пароль
    - new_password_confirm: Подтверждение нового пароля
    
    Anforderungsparameter (JSON):
    - old_password: Aktuelles Passwort
    - new_password: Neues Passwort
    - new_password_confirm: Neues Passwort bestätigen
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordDTO(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password successfully changed"}, status=status.HTTP_200_OK)

class CurrentUserAPIView(APIView):
    """
    Возвращает сведения о текущем аутентифицированном пользователе.
    
    Gibt Informationen über den aktuell authentifizierten Benutzer zurück.
    
    Возвращаемые поля:
    - id: ID пользователя
    - username: Имя пользователя
    - email: Электронная почта
    - first_name: Имя
    - last_name: Фамилия
    - profile: Профиль пользователя
    
    Rückgabefelder:
    - id: Benutzer-ID
    - username: Benutzername
    - email: E-Mail
    - first_name: Vorname
    - last_name: Nachname
    - profile: Benutzerprofil
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated:
            # стандартное сообщение DRF
            raise NotAuthenticated()

        serializer = DetailedUserDTO(user)
        return Response(serializer.data)
