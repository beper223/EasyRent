from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from src.apartments.services import SearchService
from src.apartments.dtos import SearchHistoryDTO, PopularSearchDTO


class PopularSearchesAPIView(APIView):
    """Вывод популярных запросов /
    Ausgabe der beliebtesten Suchanfragen"""

    permission_classes = [AllowAny]

    def get(self, request):
        popular = SearchService.get_popular(limit=10)
        serializer = PopularSearchDTO(popular, many=True)
        return Response(serializer.data)


class MySearchHistoryAPIView(APIView):
    """История поиска текущего арендатора /
    Suchhistorie des aktuellen Mieters"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = SearchService.my_search(request.user, limit=20)
        serializer = SearchHistoryDTO(history, many=True)
        return Response(serializer.data)
