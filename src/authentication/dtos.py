from rest_framework import serializers
from django.contrib.auth.models import User

from src.choices import UserRole


class CreateUserDTO(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserRole.choices, default=UserRole.TENANT, write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            'repeat_password',
            "role"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs: dict) -> dict:
        password = attrs.get('password')
        repeat_password = attrs.pop('repeat_password')

        if password != repeat_password:
            raise serializers.ValidationError({
                "password": "Passwords do not match"
            })

        return attrs

    def create(self, validated_data):
        role = validated_data.pop("role", UserRole.TENANT)
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # обновляем профиль ролью
        user.profile.role = role
        user.profile.save()

        return user
