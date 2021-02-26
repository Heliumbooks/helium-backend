from django.urls import path

from helium_backend.libraries.api import LibrariesList

urlpatterns = [
    path('', LibrariesList.as_view(), name='library-list')
]