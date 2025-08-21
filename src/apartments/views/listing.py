from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter
from django.db.models import Q

from src.apartments.models import Listing
from src.apartments.dtos import ListingDTO, ListingCompactDTO
from src.permissions import IsLandlordOrAdmin


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
    queryset = Listing.objects.all()
    serializer_class = ListingDTO
    permission_classes = [IsLandlordOrAdmin]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_class = ListingFilter
    search_fields = ["title", "description"]  # Suche nach Schlüsselwörtern
    ordering_fields = ["price", "created_at"]  # Sortierung nach Preis und Erstellungsdatum
    ordering = ["-created_at"]  # standardmäßig neue Einträge zuerst

    def perform_create(self, serializer):
        serializer.save(
            landlord=self.request.user,  # Eigentümer zuweisen
            is_active=True  # Anzeige automatisch aktiv setzen
        )

    def get_queryset(self):
        user = self.request.user
        qs = Listing.objects.all()

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

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_listings(self, request):
        """Vermieter sehen nur ihre eigenen Anzeigen"""
        qs = self.queryset.filter(landlord=request.user)
        serializer = ListingCompactDTO(qs, many=True)
        return Response(serializer.data)
