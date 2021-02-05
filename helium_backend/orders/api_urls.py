from django.urls import path

from helium_backend.orders.api import OrderCreate
from helium_backend.orders.api import AllOrderList
from helium_backend.orders.api import OrderAddressSelection

urlpatterns = [
    path('all-orders/', AllOrderList.as_view()),
    path('create/', OrderCreate.as_view()),
    path('create/<int:pk>/address/', OrderAddressSelection.as_view())
]
