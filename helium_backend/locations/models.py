from django.db import models
from enum import Enum

from helium_backend.users.models import User


class Timezone(Enum):
    eastern = "America/New_York"
    central = "America/Chicago"
    pacific = "America/Los_Angeles"


class AddressType(Enum):
    library = "Library"
    delivery = "Delivery"
    pick_up = "Pick Up"


class State(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = "States"
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, choices=[(timezone.value, timezone.name.title()) for timezone in Timezone])

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"


class Address(models.Model):
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    street_address = models.TextField(blank=True, null=True, default='')
    additional_street_address = models.TextField(blank=True, null=True, default='')
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    zip_code = models.CharField(max_length=12)
    type = models.CharField(max_length=50,
                            choices=[(address_type.value, address_type.name.title()) for address_type in AddressType])
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street_address} - {self.city.name}"
