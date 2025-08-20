from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from src.apartments.models import Listing
from src.apartments.dtos import ListingDTO
from src.permissions import IsLandlordOrAdmin


class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingDTO
    permission_classes = [IsAuthenticatedOrReadOnly, IsLandlordOrAdmin]

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)