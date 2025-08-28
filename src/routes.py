from django.urls import path, include
from src.apartments.views import PopularSearchesAPIView, MySearchHistoryAPIView

app_name = 'EasyRent'
urlpatterns = [
    path('users/', include('src.authentication.urls'), name='users'),
    path('listings/', include('src.apartments.urls'), name='listings'),
    path('bookings/', include('src.booking.urls'), name='bookings'),
    path("search/popular/", PopularSearchesAPIView.as_view(), name="popular-searches"),
    path("search/my/", MySearchHistoryAPIView.as_view(), name="my-search-history"),
]
