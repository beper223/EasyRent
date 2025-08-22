import time
from datetime import datetime, timezone
from typing import Callable, Optional

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError


class JWTAuthMiddleware:
    """Middleware для автообновления access-токена
    / Middleware zur automatischen Erneuerung des Access-Tokens
    """

    # За сколько секунд до истечения обновляем
    # / In wie vielen Sekunden vor Ablauf erneuern
    refresh_window_seconds: int = 60

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        access_cookie = request.COOKIES.get("access")
        refresh_cookie = request.COOKIES.get("refresh")

        minted_access: Optional[str] = None
        access_expiry_dt: Optional[datetime] = None

        if access_cookie:
            # Авторизация через access / Authentifizierung mit Access
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_cookie}"

            if self._is_access_expiring(access_cookie):
                # access скоро истечет → обновляем через refresh
                # Access läuft bald ab → mit Refresh erneuern
                if refresh_cookie:
                    minted_access, access_expiry_dt = self._mint_new_access(refresh_cookie)
                else:
                    # access истёк, refresh нет → пользователь аноним
                    # Access abgelaufen, kein Refresh → Benutzer anonym
                    pass

        elif refresh_cookie:
            # access нет, но refresh жив → выпускаем новый access
            # Access fehlt, aber Refresh gültig → neues Access ausstellen
            minted_access, access_expiry_dt = self._mint_new_access(refresh_cookie)

        # если minted_access появился → подменяем токен в запросе
        # wenn minted_access existiert → Token in der Anfrage ersetzen
        if minted_access:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {minted_access}"

        response = self.get_response(request)

        # сохраняем новый access в куки
        # neuen Access im Cookie speichern
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

    def _mint_new_access(self, refresh_token: str) -> tuple[Optional[str], Optional[datetime]]:
        """Выпуск нового access-токена / Ausstellung eines neuen Access-Tokens"""
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            exp_ts = AccessToken(new_access).get("exp")
            expiry = datetime.fromtimestamp(exp_ts, timezone.utc)
            return new_access, expiry
        except TokenError:
            # refresh тоже протух → logout
            # Refresh ebenfalls abgelaufen → Logout
            raise self._force_logout()

    def _is_access_expiring(self, access_token_str: str) -> bool:
        """Проверяем, скоро ли истечет access / Prüfen, ob Access bald abläuft"""
        try:
            token = AccessToken(access_token_str)
            exp_ts = int(token.get("exp"))
            now_ts = int(time.time())
            return exp_ts <= now_ts + self.refresh_window_seconds
        except Exception:
            return True

    def _force_logout(self):
        """Принудительный logout при истекшем refresh / Zwangs-Logout bei abgelaufenem Refresh"""
        response = JsonResponse({"detail": "Session expired. Please log in again."}, status=401)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
