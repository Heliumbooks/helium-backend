from django.contrib import admin
from .models import Library
from .models import LibraryCard

admin.site.register(Library)
admin.site.register(LibraryCard)
