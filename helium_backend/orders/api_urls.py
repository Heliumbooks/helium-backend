from django.urls import path

from helium_backend.orders.api import OrderCreate
from helium_backend.orders.api import AllOrderList

urlpatterns = [
    path('create/', OrderCreate.as_view()),
    path('all-orders/', AllOrderList.as_view())
]
