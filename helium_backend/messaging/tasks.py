from helium_backend.orders.models import Order, BookOrder
from helium_backend.messaging.models import AutomatedMessage, AutomatedMessageType


def no_books_available_message():
    pass


def all_books_available_message():
    pass


def some_books_available_message(order_id):
    message = AutomatedMessage.objects.filter()