from enum import Enum
from django.db import models


class AutomatedMessageType(Enum):
    no_books_available_confirmation = "No Books - Confirmation"
    some_books_available_confirmation = "Some Books - Confirmation"
    all_books_available_confirmation = "All Books - Confirmation"
    order_delivered = "Order Delivered"
    two_day_reminder = "Two Day Reminder"
    due_today_reminder = "Due Today Reminder"
    late_reminder = "Late Reminder"
    surpassed_late_limit = "Surpassed Late Limit"
    books_picked_up = "Books Picked Up"
    return_confirmation = "Return Confirmation"


class AutomatedMessage(models.Model):
    type = models.CharField(max_length=50, choices=[(
        message_type.value, message_type.name.title()) for message_type in AutomatedMessageType])
    email_subject = models.CharField(max_length=255, default='', blank=True)
    email_body = models.TextField(default='', blank=True)

    class Meta:
        verbose_name_plural = "Automated Messages"

    def __str__(self):
        return self.type

