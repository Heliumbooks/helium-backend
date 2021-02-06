from enum import Enum

from django.db import models
from django.contrib.postgres.fields import ArrayField

from datetime import datetime, date
from helium_backend.users.models import User
from helium_backend.customers.models import Customer
from helium_backend.books.models import Book
from helium_backend.locations.models import Address


class Status(Enum):
    incomplete = "Incomplete"
    placed = "Order Placed"
    awaiting_library_pick_up = "Awaiting Library Pick Up"
    awaiting_delivery = "Awaiting Delivery"
    awaiting_customer_pick_up = "Awaiting Customer Pick Up"
    awaiting_library_return = "Awaiting Library Return"
    completed = "Completed"
    denied = "Denied"
    overdue = "Overdue"
    lost = "Lost"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    order_initiated = models.DateTimeField(null=True, blank=True)
    order_placed = models.DateTimeField(null=True, blank=True)
    drop_off_time = models.DateTimeField(null=True, blank=True)
    drop_off_location = models.TextField(default='', null=True, blank=True)
    drop_off_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    drop_off_deadline = models.DateTimeField(null=True, blank=True)
    delivery_driver = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                        related_name='delivery_driver', null=True, blank=True)
    pick_up_driver = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                       related_name='pick_up_driver', null=True, blank=True)
    pick_up_deadline = models.DateTimeField(null=True, blank=True)
    library_pick_up_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    return_pick_up_time = models.DateTimeField(null=True, blank=True)
    returned_time = models.DateTimeField(null=True, blank=True)
    completed_by_customer = models.BooleanField(default=False)
    payment_information_submitted = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.customer.full_name} - {self.id}"


class BookOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, null=True, blank=True)
    title = models.CharField(max_length=255, default='', null=True, blank=True)
    author = models.CharField(max_length=255, default='', null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True, default='',
                              choices=[(status.value, status.name.title()) for status in Status])
    order_placed = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    library_pick_up_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True,  blank=True)
    return_pick_up_time = models.DateTimeField(null=True, blank=True)
    returned_time = models.DateTimeField(null=True, blank=True)
    pick_up_location = models.TextField(default='', null=True, blank=True)
    returned = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Book Orders"

    def __str__(self):
        return f"{self.order.customer.full_name} - {self.book.title} - {self.order_placed.date()}"