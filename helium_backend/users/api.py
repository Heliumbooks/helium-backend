from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from helium_backend.users.models import User


class UserById(APIView):

    def get(self, request, pk):
        """Endpoint to get the user's account information"""
        pass

    def patch(self, request, pk):
        """Endpoint to update a User's information"""

