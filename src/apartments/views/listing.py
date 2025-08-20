from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter
from django.db.models import Q

from src.apartments.models import Listing
from src.apartments.dtos import ListingDTO
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
        fields = ["min_price", "max_price", "min_rooms", "max_rooms", "location", "housing_type"]

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
    search_fields = ["title", "description"]  # поиск по ключевым словам
    ordering_fields = ["price", "created_at"]  # сортировка по цене и дате добавления
    ordering = ["-created_at"]  # по умолчанию новые сверху

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)

    def get_queryset(self):
        user = self.request.user
        qs = Listing.objects.all()

        if not user.is_authenticated:
            # неавторизованные видят только активные
            return qs.filter(is_active=True)

        if user.is_staff:
            # администраторы видят всё
            return qs

        if hasattr(user, "profile") and user.profile.role == "landlord":
            # арендодатель видит все свои объявления + чужие активные
            return qs.filter(Q(is_active=True) | Q(landlord=user))

        # остальные (например, арендаторы) видят только активные
        return qs.filter(is_active=True)