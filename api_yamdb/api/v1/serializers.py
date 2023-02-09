import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


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
        year = datetime.date.today().year
        if not value <= year:
            raise serializers.ValidationError(
                'Нельзя добавить произведение из будущего!')
        return value


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True, required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',)
        model = Title
        read_only = ('id', 'rating', 'category', 'genre',)

    def get(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.get(**validated_data)
            return title
        else:
            genres = validated_data.pop('genre')
            title = Title.objects.get(**validated_data)
            for genre in genres:
                current_genre, status = Genre.objects.get(
                    **genre)
                GenreTitle.objects.get(
                    genre=current_genre, title=title)
            return title

    def validate_year(self, value):
        year = datetime.date.today().year
        if not value <= year:
            raise serializers.ValidationError(
                'Нельзя добавить произведение из будущего!')
        return value


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
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = self.context['request'].user
        if not request.method == 'POST':
            return data
        if title.reviews.filter(author=author).exists():
            raise serializers.ValidationError(
                'Можно оставить только 1 отзыв на произведение!')
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
