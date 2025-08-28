from rest_framework import serializers
from src.apartments.models import SearchHistory


class SearchHistoryDTO(serializers.ModelSerializer):
    """Сериализатор для истории поиска /
    Serializer für die Suchhistorie"""

    class Meta:
        model = SearchHistory
        fields = ["keyword", "created_at", "search_count"]


class PopularSearchDTO(serializers.Serializer):
    """Сериализатор для популярных запросов /
    Serializer für beliebte Suchanfragen"""

    keyword = serializers.CharField()
    total = serializers.IntegerField()