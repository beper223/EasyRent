from django.db.models import F, Sum
from src.apartments.models import SearchHistory


class SearchService:
    """Сервис для работы с историей поиска / Service zur Verwaltung der Suchhistorie"""

    @staticmethod
    def log_search(user, keyword: str):
        """Записывает новый запрос или увеличивает счётчик /
        Speichert eine neue Suche oder erhöht den Zähler"""
        obj, created = SearchHistory.objects.get_or_create(
            user=user if user.is_authenticated else None,
            keyword=keyword
        )
        if not created:
            obj.search_count = F("search_count") + 1
            obj.save(update_fields=["search_count"])
            obj.refresh_from_db(fields=["search_count"])
        # return obj

    @staticmethod
    def get_popular(limit: int = 10):
        """Возвращает популярные поисковые запросы /
        Gibt die beliebtesten Suchanfragen zurück"""
        return (
            SearchHistory.objects
            .values("keyword")
            .annotate(total=Sum("search_count"))
            .order_by("-total")[:limit]
        )

    @staticmethod
    def my_search(user, limit: int = 20):
        """Возвращает историю поиска текущего пользователя-арендатора /
        Gibt die Suchhistorie des aktuellen Mieters zurück"""
        if not user.is_authenticated:
            return SearchHistory.objects.none()

        # Проверка роли пользователя
        if not hasattr(user, "profile") or user.profile.role != "tenant":
            return SearchHistory.objects.none()

        return (
            SearchHistory.objects
            .filter(user=user)
            .order_by("-created_at")[:limit]
        )
