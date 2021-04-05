from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from helium_backend.users.models import User


class UserById(APIView):

    def get(self, request, pk):
        user = request.user
        retrieved_user = User.objects.filter(pk=user.id).first()
        if not retrieved_user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        response = {
            "first_name": retrieved_user.first_name,
            "last_name": retrieved_user.last_name,
            "email": retrieved_user.email,
            "contact_email_address": retrieved_user.contact_email_address,
            "store_addresses": retrieved_user.store_addresses,
            "store_cards": retrieved_user.store_cards,
            "public_book_reviews": retrieved_user.public_book_reviews
        }

        return Response(response)

    def patch(self, request, pk):
        """Endpoint to update a User's information"""

