from typing import Callable, Optional
from datetime import datetime, timezone
import time

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError


class JWTAuthMiddleware:
    """Middleware для автообновления access-токена / Middleware zur automatischen Erneuerung des Access-Tokens"""

    # за сколько секунд до истечения обновляем / In wie vielen Sekunden vor Ablauf erneuern
    refresh_window_seconds: int = 60

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        try:
            access_cookie = request.COOKIES.get("access")
            refresh_cookie = request.COOKIES.get("refresh")

            minted_access: Optional[str] = None
            access_expiry_dt: Optional[datetime] = None

            if access_cookie:
                # Авторизация через access / Authentifizierung mit Access
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_cookie}"

                if self._is_access_expiring(access_cookie) and refresh_cookie:
                    # access скоро истечет → обновляем через refresh
                    # Access läuft bald ab → mit Refresh erneuern
                    minted_access, access_expiry_dt = self._mint_new_access(refresh_cookie)

            elif refresh_cookie:
                # access нет, но refresh жив → выпускаем новый access
                # Access fehlt, aber Refresh gültig → neues Access ausstellen
                minted_access, access_expiry_dt = self._mint_new_access(refresh_cookie)

            if minted_access:
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {minted_access}"

            response = self.get_response(request)

            if minted_access:
                response.set_cookie(
                    key="access",
                    value=minted_access,
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                    expires=access_expiry_dt,
                )

            return response

        except PermissionDenied:
            # При истекшем refresh возвращаем JsonResponse и удаляем куки
            # Bei abgelaufenem Refresh JsonResponse zurückgeben und Cookies löschen
            response = JsonResponse({"detail": "Session expired. Please log in again."}, status=401)
            response.delete_cookie("access")
            response.delete_cookie("refresh")
            return response

    def _mint_new_access(self, refresh_token: str) -> tuple[Optional[str], Optional[datetime]]:
        # Выпуск нового access-токена
        # Ausstellung eines neuen Access-Tokens
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            exp_ts = AccessToken(new_access).get("exp")
            expiry = datetime.fromtimestamp(exp_ts, timezone.utc)
            return new_access, expiry
        except TokenError:
            # refresh истёк → выбрасываем исключение
            # Refresh ist abgelaufen → Ausnahme werfen
            raise PermissionDenied("Refresh token expired, user logged out")

    def _is_access_expiring(self, access_token_str: str) -> bool:
        # Проверяем, скоро ли истечет access
        # Prüfen, ob Access bald abläuft
        try:
            token = AccessToken(access_token_str)
            exp_ts = int(token.get("exp"))
            now_ts = int(time.time())
            return exp_ts <= now_ts + self.refresh_window_seconds
        except Exception:
            return True
