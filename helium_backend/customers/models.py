from django.db import models
from django.contrib.postgres.fields import ArrayField

from helium_backend.users.models import User


class Customer(models.Model):
    first_name = models.CharField(max_length=100, default='', null=True, blank=True)
    last_name = models.CharField(max_length=100, default='', null=True, blank=True)
    full_name = models.CharField(max_length=200, default='', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    phone_numbers = ArrayField(models.CharField(max_length=20, default='', blank=True), default=list)
    emails = ArrayField(models.CharField(max_length=200, default='', blank=True), default=list)
    orders = models.IntegerField(default=0)
    referrals = models.IntegerField(default=0)
    referral_code = models.CharField(max_length=100, default='', blank=True, null=True)
    referred_by_code = models.CharField(max_length=100, default='', blank=True, null=True)

    class Meta:
        verbose_plural_name = "Customers"
        ordering = ('full_name',)

    def __str__(self):
        return f"{self.full_name}"
