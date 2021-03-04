from django.urls import path

from helium_backend.libraries.api import LibrariesList
from helium_backend.libraries.api import LibraryCardList

urlpatterns = [
    path('', LibrariesList.as_view(), name='library-list'),
    path('cards/', LibraryCardList.as_view(), name='library-cards')
]