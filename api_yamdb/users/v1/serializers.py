import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class RegisterDataSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
    )

    class Meta:
        fields = ("username", "email")
        model = User

    def validate(self, data):
        if data['username'] == 'me':
            raise ValidationError(
                {'Имя пользователя не может быть <me>.'})
        if re.search(
            r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', data['username'].lower()
        ) is None:
            raise ValidationError(
                ('Недопустимые символы в username!'),
            )
        user = User.objects.filter(
            username=data.get('username')
        )
        email = User.objects.filter(
            email=data.get('email')
        )
        if not user.exists() and email.exists():
            raise ValidationError("Недопустимый Email")
        if user.exists() and user.get().email != data.get('email'):
            raise ValidationError("Недопустимый Email")
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
