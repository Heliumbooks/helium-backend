from django.urls import path

from helium_backend.users.api import UserById

urlpatterns = [
    path('<int:pk>', UserById.as_view(), name="user-details")
]
