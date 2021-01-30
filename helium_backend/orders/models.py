from django.db import models
from datetime import datetime, date
from helium_backend.users.models import User
from helium_backend.customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    order_time = models.DateTimeField(null=True, blank=True)
    drop_off_time = models.DateTimeField(null=True, blank=True)
    drop_off_location = models.TextField(default='', null=True, blank=True)
    delivery_driver = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pick_up_driver = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    library_pick_up_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    return_pick_up_time = models.DateTimeField(null=True, blank=True)
    returned_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.customer.full_name} - {self.order_time.date()}"
