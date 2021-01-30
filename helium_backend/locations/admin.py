from django.contrib import admin
from .models import State
from .models import City
from .models import Address


admin.site.register(State)


admin.site.register(City)


admin.site.register(Address)