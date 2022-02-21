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


class Subject(models.Model):
    title = models.TextField(default='', null=True, blank=True)
    books_in_subject = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Subjects"
        ordering = ('title',)
    
    def __str__(self):
        return f"{self.title}"


class Book(models.Model):
    title = models.CharField(max_length=255, default='', null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, null=True, blank=True)
    genre = models.CharField(max_length=50, null=True, blank=True, default='',
                             choices=[(genre.value, genre.name.title()) for genre in Genre])
    pages = models.IntegerField(default=0)
    requests = models.IntegerField(default=0)
    isbn = models.TextField(default='', null=True, blank=True)
    lexile_score = models.CharField(max_length=50, default='', null=True, blank=True)
    synopsis = models.TextField(default='', null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    average_book_rating = models.FloatField(default=0)
    processed_from_open_lib = models.BooleanField(default=False)
    subjects = models.ManyToManyField(Subject, blank=True)
    book_ol_id = models.CharField(max_length=200, default='', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Books"
        ordering = ('title',)

    def __str__(self):
        return f"{self.title}"


class IsbnNumber(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, null=True, blank=True)
    isbn = models.TextField(default='', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Isbn Numbers"
    
    def __str__(self):
        return f"{self.isbn}"


