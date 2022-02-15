from django.urls import path 

from helium_backend.books.api import DatabaseLoad, DatabaseUpdate

urlpatterns = [
    path('seed/', DatabaseLoad.as_view()),
    path('update/', DatabaseUpdate.as_view())
]