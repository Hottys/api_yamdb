from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import LETTERS_IN_STR

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=56)

    def __str__(self):
        return self.name[:LETTERS_IN_STR]


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=56)

    def __str__(self):
        return self.name[:LETTERS_IN_STR]


class Title(models.Model):
    '''Поле rating временно опущено.'''
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )

    def __str__(self):
        return self.name[:LETTERS_IN_STR]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre[:LETTERS_IN_STR]} {self.title[:LETTERS_IN_STR]}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('text', 'author',),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text
