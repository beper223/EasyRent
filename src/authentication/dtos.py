from rest_framework import serializers
from django.contrib.auth.models import User

from src.choices import UserRole


class CreateUserDTO(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserRole.choices, default=UserRole.TENANT, write_only=True)
    repeat_password = serializers.CharField(
        write_only=True,
        required=True,
    )

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

    def update(self, instance, validated_data):
        role = validated_data.pop("role", None)
        password = validated_data.pop("password", None)

        # обновляем стандартные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        # менять роль может только админ
        request = self.context.get("request")
        if role and request and request.user.is_staff:
            instance.profile.role = role
            instance.profile.save()

        return instance

class ListUsersDTO(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        if instance.profile:
            resp['role'] = instance.profile.role
        else:
            resp['role'] = None
        return resp

class DetailedUserDTO(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_active",
            "is_staff",
            "date_joined",
            "groups",
            "user_permissions"
        )