from django.db import models

from helium_backend.customers.models import Customer


class StripeClient(models.Model):
    api_key = models.CharField(max_length=200, null=True, blank=True)


class StripeProduct(models.Model):
    name = models.CharField(max_length=200)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=False)
    description = models.TextField(default='', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Stripe Products"

    def __str__(self):
        return f"{self.name}"


class StripeCustomer(models.Model):
    email = models.CharField(max_length=200)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True, blank=True)
    account_balance = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Stripe Customers"

    def __str__(self):
        return f"{self.email}"


class StripeInvoice(models.Model):
    stripe_customer = models.ForeignKey(StripeCustomer, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Stripe Invoices"

    def __str__(self):
        return f"{self.stripe_customer.email} - {self.created_at}"


class StripeInvoiceItem(models.Model):
    description = models.TextField(default='', null=True, blank=True)
    stripe_invoice = models.ForeignKey(StripeInvoice, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StripeSetupIntent(models.Model):
    stripe_customer = models.ForeignKey(StripeCustomer, on_delete=models.DO_NOTHING, null=True, blank=True)
    stripe_setup_intent_id = models.CharField(max_length=200, default='', null=True, blank=True)
    stripe_client_secret = models.CharField(max_length=200, default='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Stripe Intents"

    def __str__(self):
        return f"{self.stripe_customer.customer.first_name} {self.stripe_customer.customer.last_name} - {self.created_at}"