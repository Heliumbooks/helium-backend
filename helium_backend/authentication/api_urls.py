from django.urls import path

from helium_backend.authentication.api import UserLogin

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user_login'),
]