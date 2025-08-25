from django.urls import path, include

app_name = 'EasyRent'
urlpatterns = [
    path('users/', include('src.authentication.urls'), name='users'),
    path('listings/', include('src.apartments.urls'), name='listings'),
    path('bookings/', include('src.booking.urls'), name='bookings'),
]
