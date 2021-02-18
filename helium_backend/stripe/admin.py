from django.contrib import admin
from helium_backend.stripe.models import StripeClient


admin.site.register(StripeClient)