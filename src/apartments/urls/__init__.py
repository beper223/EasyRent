from rest_framework.routers import DefaultRouter
from src.apartments.views import ListingViewSet

router = DefaultRouter()
router.register("", ListingViewSet)

urlpatterns = router.urls