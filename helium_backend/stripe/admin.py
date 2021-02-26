from django.contrib import admin
from helium_backend.stripe.models import StripeClient
from helium_backend.stripe.models import StripeSetupIntent


admin.site.register(StripeClient)
admin.site.register(StripeSetupIntent)