from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User

from src.choices import UserRole


class RegisterUserDTO(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserRole.choices, default=UserRole.TENANT, write_only=True)
    repeat_password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
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

        validate_password(password)
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
        if role == UserRole.ADMIN:
            user.is_staff = True
        user.save()

        # обновляем профиль ролью
        user.profile.role = role
        user.profile.save()

        return user


class UpdateUserDTO(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserRole.choices, default=UserRole.TENANT, write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "role"
        ]
        extra_kwargs = {
            "username": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": False},
            "role": {"required": False}
        }

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
            'first_name',
            'last_name',
            'email',
            'is_active'
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
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        )

class ChangePasswordDTO(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    repeat_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["repeat_password"]:
            raise serializers.ValidationError({"repeat_password": "Passwords do not match"})
        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user