from reviews.models import Genre, Title, Category, User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


class TtileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category
