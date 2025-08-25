from django.urls import path, include

app_name = 'EasyRent'
urlpatterns = [
    path('users/', include('src.authentication.urls')),
    path('listings/', include('src.apartments.urls')),
    path('bookings/', include('src.booking.urls')),
]
