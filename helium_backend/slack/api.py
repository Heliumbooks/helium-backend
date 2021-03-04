from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from helium_backend.slack.models import SlackChannel


class SlackWebhook(APIView):
    def post(self, request):
        data = request.data.get('message')
        channel = SlackChannel.objects.first()
        channel.send_message(data)
        return Response(status=status.HTTP_200_OK)