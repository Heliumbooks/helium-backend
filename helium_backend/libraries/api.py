from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from helium_backend.libraries.models import Library


class LibrariesList(APIView):
    def get(self, request):
        libraries = Library.objects.filter(active=True).values('id', 'name').order_by('name')
        return Response(libraries)
