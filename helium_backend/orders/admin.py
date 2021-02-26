from django.contrib import admin
from .models import Order
from .models import BookOrder

admin.site.register(Order)
admin.site.register(BookOrder)
