from rest_framework import generics
from django.contrib.auth.models import User
from src.authentication.dtos import CreateUserDTO


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserDTO
