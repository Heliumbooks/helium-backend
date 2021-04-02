from django.urls import path

from helium_backend.authentication.api import UserLogin
from helium_backend.authentication.api import UserRegistration

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user_login'),
    path('signup/', UserRegistration.as_view(), name='user-signup')
]