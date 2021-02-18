from django.db import models


class StripeClient(models.Model):
    api_key = models.CharField(max_length=200, null=True, blank=True)
