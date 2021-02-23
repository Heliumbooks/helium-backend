import stripe

from helium_backend.stripe.models import StripeClient
from helium_backend.stripe.models import StripeSetupIntent
from helium_backend.stripe.models import StripeCustomer

from helium_backend.customers.models import Customer


def create_customer(email, payment_method_id=None):
    client = StripeClient.objects.first()
    stripe.api_key = client.api_key

    customer = Customer.objects.filter(emails__contains=[email]).first()

    customer_data = stripe.Customer.list(email=email).data
    print(customer_data)
    if len(customer_data) == 0 and payment_method_id:
        stripe_customer = stripe.Customer.create(
            email=email,
            payment_method=payment_method_id
        )
    elif len(customer_data) == 0:
        stripe_customer = stripe.Customer.create(
            email=email
        )
    else:
        stripe_customer = customer_data[0]

    helium_stripe_customer = StripeCustomer.objects.filter(email=email).first()
    if not helium_stripe_customer:
        helium_stripe_customer = StripeCustomer.objects.create(
            email=email,
            customer=customer,
            stripe_id=stripe_customer.get('id')
        )

    return helium_stripe_customer.id


def create_payment_method(card_number, exp_month, exp_year, cvc):
    client = StripeClient.objects.first()
    stripe.api_key = client.api_key

    payment_method = stripe.PaymentMethod.create(
        type="card",
        card={
            "number": card_number,
            "exp_month": exp_month,
            "exp_year": exp_year,
            "cvc": cvc
        }
    )

    return payment_method


def create_setup_intent(customer_id):
    client = StripeClient.objects.first()
    stripe.api_key = client.api_key
    helium_stripe_customer = StripeCustomer.objects.filter(pk=customer_id).first()

    try:
        intent = stripe.SetupIntent.create(
            payment_method_types=["card"],
            customer=helium_stripe_customer.stripe_id
        )
        StripeSetupIntent.objects.create(
            stripe_customer=helium_stripe_customer,
            stripe_setup_intent_id=intent.get('id'),
            stripe_client_secret=intent.get('client_secret')
        )
    except:
        StripeSetupIntent.objects.create(
            stripe_customer=helium_stripe_customer
        )



