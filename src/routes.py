from django.urls import path, include

urlpatterns = [
    #path('listings/', include('src.apartments.urls')),
    path('users/', include('src.authentication.urls')),
]
