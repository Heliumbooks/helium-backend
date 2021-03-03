from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from helium_backend.libraries.models import Library
from helium_backend.libraries.models import LibraryCard


class LibrariesList(APIView):
    def get(self, request):
        libraries = Library.objects.filter(active=True).values('id', 'name').order_by('name')
        return Response(libraries)


class LibraryCardList(APIView):
    def get(self, request):
        library_cards = LibraryCard.objects.filter(active=True).values('id', 'name').order_by('id')
        return Response(library_cards)
