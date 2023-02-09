from django.contrib.auth import get_user_model
from api.mixins import NoPutViewSet
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.permissions import AdminOnly

from api_yamdb.settings import DEFAULT_EMAIL
from .serializers import (RegisterDataSerializer, TokenSerializer,
                          UserSerializer)

User = get_user_model()


@api_view(["POST"])
def user_register(request):
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        **serializer.validated_data
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="Регистрация",
        message=f"Ваш код подтверждения: {confirmation_code}",
        from_email=DEFAULT_EMAIL,
        recipient_list=[user.email],
    )
    return Response(
        serializer.data, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get("username")
    )
    if default_token_generator.check_token(
        user, serializer.validated_data.get("confirmation_code")
    ):
        token = AccessToken.for_user(user)
        return Response(
            {"token": str(token)}, status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(NoPutViewSet):
    lookup_field = ('username')
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOnly,)
    search_fields = ('username',)
    lookup_field = ('username')

    @action(
        methods=[
            "GET",
            "PATCH",
        ],
        detail=False,
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def users_own_profile(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "PATCH":
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
