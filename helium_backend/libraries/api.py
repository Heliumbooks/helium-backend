from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from helium_backend.libraries.models import Library


class LibrariesList(APIView):
    def get(self, request):
        libraries = Library.objects.all()
