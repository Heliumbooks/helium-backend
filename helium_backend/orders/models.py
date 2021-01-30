from django.db import models
from datetime import datetime, date
from helium_backend.users.models import User


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order_time = models.DateTimeField(null=True, blank=True)
    drop_off_time = models.DateTimeField(null=True, blank=True)
