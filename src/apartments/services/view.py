from django.db.models import F
from django.http import HttpRequest

from src.apartments.models.listingview import ListingView
from src.apartments.models.listing import Listing

class ViewService:
    @staticmethod
    def record_view(listing: Listing, request: HttpRequest):
        """
        Учитывает просмотр объявления.
        Если пользователь уже просматривал это объявление, увеличивает счетчик.
        Иначе создает новую запись.

        Args:
            listing: Объект объявления
            request: Объект HTTP-запроса

        Returns:
            ListingView: Созданная или обновленная запись о просмотре
        """
        user = request.user if request.user.is_authenticated else None
        ip_address = request.META.get('REMOTE_ADDR')
        
        # Создаем или обновляем запись о просмотре
        view, created = ListingView.objects.get_or_create(
            listing=listing,
            user=user,
            ip_address=ip_address,
            defaults={'view_count': 1}
        )
        
        # Если запись уже существовала, увеличиваем счетчик
        if not created:
            view.view_count = F('view_count') + 1
            view.save(update_fields=['view_count'])
