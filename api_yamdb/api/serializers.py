import datetime

from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        current_year = timezone.now().year
        if not 0 <= value <= current_year:
            raise serializers.ValidationError(
                'Проверьте год создания произведения.'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if not rating:
            return rating
        return round(rating, 1)

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genre')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(
                    **genre)
                GenreTitle.objects.create(
                    genre=current_genre, title=title)
            return title

    def validate_year(self, value):
        """Год выпуска не должен быть больше текущего."""
        year = datetime.date.today().year
        if not value <= year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only = ('id',)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'К каждому произведению вы можете написать только 1 отзыв!')
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
