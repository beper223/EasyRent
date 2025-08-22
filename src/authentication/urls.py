from django.urls import path

from src.authentication.views import (
    UserListCreateView,
    UserRetrieveUpdateDestroyView,
    LoginUserAPIView,
    LogoutUserAPIView,
    ChangePasswordAPIView,
    CurrentUserAPIView
)

urlpatterns = [
    path("", UserListCreateView.as_view()),
    path("<int:pk>/", UserRetrieveUpdateDestroyView.as_view()),
    path('login/', LoginUserAPIView.as_view()),
    path('logout/', LogoutUserAPIView.as_view()),
    path("change-password/", ChangePasswordAPIView.as_view()),
    path("my", CurrentUserAPIView.as_view()),
]