from rest_framework.routers import DefaultRouter
from django.urls import path, include
from src.booking.views import BookingViewSet

router = DefaultRouter()
router.register("", BookingViewSet)

urlpatterns = router.urls