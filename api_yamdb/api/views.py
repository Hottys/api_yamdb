from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework import filters, status
from rest_framework.decorators import api_view, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Genre, Review, Title, User

from .mixins import CreateListDestroyViewSet, NoPutViewSet
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          RegisterDataSerializer, TokenSerializer,
                          UserEditSerializer, UserSerializer)
from .permissions import (AdminOnly, AdminOrReadOnly, IsAuthorOrModerOrAdmin)


class TitleViewSet(NoPutViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year',)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(NoPutViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerOrAdmin,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(NoPutViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


@api_view(["POST"])
def user_register(request):
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).exists():
        return Response(request.data, status=status.HTTP_200_OK)
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, create = User.objects.get_or_create(
            **serializer.validated_data
        )
    except IntegrityError:
        raise ValidationError("Неверное имя пользователя или email")
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="Регистрация",
        message=f"Ваш код подтверждения: {confirmation_code}",
        from_email=None,
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
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(NoPutViewSet):
    lookup_field = ('username')
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOnly,)
    search_fields = ('username',)

    @action(
        methods=[
            "GET",
            "PATCH",
        ],
        detail=False,
        url_path="me",
        permission_classes=[IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "PATCH":
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
