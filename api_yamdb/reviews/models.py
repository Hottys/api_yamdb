from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=56)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=56)
    description = models.TextField()


class Title(models.Model):
    name = models.CharField(max_length=256)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )
