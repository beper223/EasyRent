from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter
from django.db.models import Q, Count, Sum, Value
from django.db.models.functions import Coalesce

from src.apartments.models import Listing
from src.apartments.dtos import ListingDTO, ListingCompactDTO, ReviewCreateDTO, ReviewDTO, ListingDetailDTO
from src.permissions import IsLandlordOrAdmin, IsTenant
from src.apartments.services import ViewService, SearchService


class ListingFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")
    min_rooms = NumberFilter(field_name="rooms", lookup_expr="gte")
    max_rooms = NumberFilter(field_name="rooms", lookup_expr="lte")
    location = CharFilter(field_name="location", lookup_expr="icontains")
    housing_type = CharFilter(field_name="housing_type", lookup_expr="exact")

    class Meta:
        model = Listing
        fields = [
            "min_price",
            "max_price",
            "min_rooms",
            "max_rooms",
            "location",
            "housing_type"
        ]

class ListingViewSet(ModelViewSet):
    """
    ViewSet для работы с объявлениями о недвижимости.
    Позволяет просматривать, создавать, обновлять и удалять объявления.
    
    ViewSet für Immobilienanzeigen.
    Ermöglicht das Anzeigen, Erstellen, Aktualisieren und Löschen von Anzeigen.
    
    Поля:
    - title: Заголовок объявления
    - description: Описание
    - price: Цена за сутки
    - location: Местоположение
    - rooms: Количество комнат
    - housing_type: Тип жилья (APARTMENT/HOUSE/VILLA)
    - is_active: Активно ли объявление
    
    Felder:
    - title: Anzeigentitel
    - description: Beschreibung
    - price: Preis pro Tag
    - location: Standort
    - rooms: Anzahl der Zimmer
    - housing_type: Wohnungstyp (APARTMENT/HAUS/VILLA)
    - is_active: Ist die Anzeige aktiv
    """
    queryset = Listing.objects.all()
    permission_classes = [IsLandlordOrAdmin]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_class = ListingFilter
    search_fields = ["title", "description", "location"]  # Suche nach Schlüsselwörtern
    ordering_fields = ["price", "created_at", "views_count", "reviews_count"]  # Sortierung nach Preis und Erstellungsdatum
    ordering = ["-created_at"]  # standardmäßig neue Einträge zuerst

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от действия.
        Для детального просмотра возвращает ListingDetailDTO с отзывами,
        для списка - ListingDTO без отзывов.
        
        Gibt den Serializer je nach Aktion zurück.
        Für die Detailansicht wird ListingDetailDTO mit Bewertungen zurückgegeben,
        für die Liste ListingDTO ohne Bewertungen.
        """
        if self.action == "retrieve":
            return ListingDetailDTO  # детальный просмотр с отзывами
        return ListingDTO  # список без отзывов

    def perform_create(self, serializer):
        """
        Создает новое объявление.
        Устанавливает текущего пользователя как владельца и делает объявление активным.
        
        Erstellt eine neue Anzeige.
        Setzt den aktuellen Benutzer als Eigentümer und aktiviert die Anzeige.
        """
        serializer.save(
            landlord=self.request.user,  # Eigentümer zuweisen
            is_active=True  # Anzeige automatisch aktiv setzen
        )

    def get_queryset(self):
        """
        Возвращает queryset объявлений в зависимости от прав пользователя.
        - Неаутентифицированные пользователи: только активные объявления
        - Администраторы: все объявления
        - Арендодатели: свои объявления + активные чужие
        - Остальные: только активные объявления
        
        Gibt einen QuerySet von Anzeigen zurück, abhängig von den Benutzerrechten.
        - Nicht authentifizierte Benutzer: nur aktive Anzeigen
        - Administratoren: alle Anzeigen
        - Vermieter: eigene Anzeigen + aktive anderer
        - Andere: nur aktive Anzeigen
        """
        user = self.request.user
        qs = (
            Listing.objects.all()
            .annotate(
                views_count=Coalesce(Sum("views__view_count"), Value(0)),
                reviews_count=Count("reviews", distinct=True)
            )
        )

        # --- сохраняем поисковый запрос ---
        keyword = self.request.query_params.get("search")
        if keyword:
            SearchService.log_search(user, keyword)

        if not user.is_authenticated:
            # nicht authentifizierte Benutzer sehen nur aktive Anzeigen
            return qs.filter(is_active=True)

        if user.is_staff:
            # Administratoren sehen alle Anzeigen
            return qs

        if hasattr(user, "profile") and user.profile.role == "landlord":
            # Vermieter sehen alle eigenen Anzeigen + andere aktive
            return qs.filter(Q(is_active=True) | Q(landlord=user))

        # andere (z.B. Mieter) sehen nur aktive Anzeigen
        return qs.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        """
        Возвращает детали объявления.
        Учитывает просмотры для аутентифицированных и анонимных пользователей.
        
        Gibt die Details einer Anzeige zurück.
        Berücksichtigt Ansichten von authentifizierten und anonymen Benutzern.
        """
        listing = self.get_object()
        
        # Учитываем просмотр, если пользователь не владелец объявления
        if not request.user.is_authenticated or request.user.id != listing.landlord_id:
            ViewService.record_view(listing, request)

        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_listings(self, request):
        """
        Возвращает список объявлений текущего пользователя.
        Доступно только аутентифицированным пользователям.
        
        Gibt die Liste der Anzeigen des aktuellen Benutzers zurück.
        Nur für authentifizierte Benutzer verfügbar.
        """
        # Используем get_queryset() для получения аннотаций, затем фильтруем по текущему пользователю
        qs = self.get_queryset().filter(landlord=request.user)
        serializer = ListingCompactDTO(qs, many=True) 
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsTenant])
    def add_review(self, request, pk=None):
        """
        Добавляет отзыв к объявлению.
        Доступно только для арендаторов, которые завершили бронирование.
        
        Fügt eine Bewertung zur Anzeige hinzu.
        Nur für Mieter verfügbar, die eine abgeschlossene Buchung haben.
        
        Параметры (в теле запроса):
        - rating: Оценка (1-5)
        - comment: Текст отзыва (опционально)
        
        Parameter (im Request-Body):
        - rating: Bewertung (1-5)
        - comment: Bewertungstext (optional)
        """
        listing = self.get_object()

        serializer = ReviewCreateDTO(
            data=request.data, context={"request": request, "listing": listing}
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(ReviewCreateDTO(review).data, status=status.HTTP_201_CREATED)
