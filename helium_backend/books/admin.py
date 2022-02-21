from django.contrib import admin
from .models import Author
from .models import Book
from .models import IsbnNumber
from .models import Subject


admin.site.register(Author)


admin.site.register(Book)


admin.site.register(IsbnNumber)


admin.site.register(Subject)

