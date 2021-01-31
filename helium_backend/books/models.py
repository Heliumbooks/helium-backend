from enum import Enum

from django.db import models


class Genre(Enum):
    horror = "Horror"
    science_fiction = "Science Fiction"
    non_fiction = "Non Fiction"


class Author(models.Model):
    first_name = models.CharField(max_length=100, default='', null=True, blank=True)
    last_name = models.CharField(max_length=100, default='', null=True, blank=True)
    full_name = models.CharField(max_length=200, default='', null=True, blank=True)
    information = models.TextField(default='', null=True, blank=True)
    orders = models.IntegerField(default=0)
    cost = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Authors"
        ordering = ('full_name',)

    def __str__(self):
        return f"{self.full_name}"


class Book(models.Model):
    title = models.CharField(max_length=255, default='', null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, null=True, blank=True)
    genre = models.CharField(max_length=50, null=True, blank=True, default='',
                             choices=[(genre.value, genre.name.title()) for genre in Genre])
    pages = models.IntegerField(default=0)
    requests = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Books"
        ordering = ('title',)

    def __str__(self):
        return f"{self.title}"


