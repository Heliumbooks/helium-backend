from django.urls import path
from helium_backend.stripe.api import TestPayment
from helium_backend.stripe.api import SaveStripeInfo
from helium_backend.stripe.api import CreatePayment
from helium_backend.stripe.api import ProcessInvoice

urlpatterns = [
    path('test/', TestPayment.as_view()),
    path('save-info/', SaveStripeInfo.as_view()),
    path('create-payment/', CreatePayment.as_view()),
    path('invoice/', ProcessInvoice.as_view())
]