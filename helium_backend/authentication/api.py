from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.utils import timezone

from helium_backend.users.models import User, UserPassword


class UserLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': f'Bearer {token.key}',
            'id': user.pk,
            'email': user.email,
            'is_admin': user.is_admin,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


class UserRegistration(APIView):

    def post(self, request):
        """Endpoint to register a user with a email and password"""
        if not request.data.get('email'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not request.data.get('password'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        current_date = timezone.now().date()
        try:

            user = User.objects.create_user(
                email=request.data.get('email'),
                password=request.data.get('password'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                date_joined=current_date
            )

            UserPassword.objects.create(
                user=user,
                password_hash=user.password
            )

            token, created = Token.objects.get_or_create(user=user)
            response =({
                "token": f'Bearer {token.key}',
                "id": user.pk,
                "email": user.email,
                "is_admin": user.is_admin,
                "first_name": user.first_name,
                "last_name": user.last_name
            })
            return Response(status=status.HTTP_201_CREATED, data=response)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)