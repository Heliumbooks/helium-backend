from django.urls import path 

from helium_backend.books.api import DatabaseUpdate
# from helium_backend.books.api import DatabaseLoad, UpdateBookInfo

urlpatterns = [
    # path('seed/', DatabaseLoad.as_view()),
    path('update/', DatabaseUpdate.as_view()),
    # path('book-info-update/', UpdateBookInfo.as_view())
]