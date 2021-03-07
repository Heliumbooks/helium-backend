from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from helium_backend.slack.models import SlackChannel
from helium_backend.orders.tasks import send_pending_order_notification, daily_library_pickups, daily_customer_pickups, \
    send_renewal_request_notification, daily_overdue_books


class SlackWebhook(APIView):
    def post(self, request):
        daily_overdue_books()
        return Response(status=status.HTTP_200_OK)
