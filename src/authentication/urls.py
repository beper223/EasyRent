from django.urls import path

from src.authentication.views import (
    UserListCreateView,
    UserRetrieveUpdateDestroyView,
    LoginUserAPIView,
    LogoutUserAPIView,
)

urlpatterns = [
    path("", UserListCreateView.as_view(), name="user-list-create"),
    path("<int:pk>/", UserRetrieveUpdateDestroyView.as_view(), name="user-detail"),
    path('login/', LoginUserAPIView.as_view()),
    path('logout/', LogoutUserAPIView.as_view()),
]