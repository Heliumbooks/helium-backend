from django.db import models

from helium_backend.locations.models import Address


class Library(models.Model):
    name = models.CharField(max_length=200, default='', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Libraries"
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"

