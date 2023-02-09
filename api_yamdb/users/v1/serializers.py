from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from users.validators import validate_username

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
        validators=(validate_username,),
    )

    class Meta:
        fields = ("username", "email")
        model = User

    def validate(self, data):
        if data['username'] == 'me':
            raise ValidationError(
                {'Имя пользователя не может быть <me>.'})
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
