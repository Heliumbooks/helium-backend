from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe

from helium_backend.stripe.models import StripeClient
from helium_backend.stripe.models import StripeSetupIntent


class CreatePayment(APIView):
    def post(self, request):
        client = StripeClient.objects.first()

        stripe.api_key = client.api_key

        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": request.data.get('cardNumber'),
                "exp_month": request.data.get('expirationMonth'),
                "exp_year": request.data.get('expirationYear'),
                "cvc": request.data.get('cvc')
            }
        )

        customer_data = stripe.Customer.list(email=request.data.get('email')).data

        message = ""
        if len(customer_data) == 0:
            customer = stripe.Customer.create(
                email=request.data.get('email'),
                payment_method=payment_method.get('id')
            )
        else:
            customer = customer_data[0]
            message = "Customer already existed"

        intent = stripe.PaymentIntent.create(
            customer=customer,
            payment_method=payment_method.get('id'),
            currency='usd',
            amount=300,
            confirm=True
        )

        response = {
            'message': 'Success',
            'data': {
                "customer_id": customer.id,
                "extra_message": message,
                "intent": intent.get('id')
            }
        }

        return Response(status=status.HTTP_200_OK, data=response)


class ProcessInvoice(APIView):
    def post(self, request):
        client = StripeClient.objects.first()
        stripe.api_key = client.api_key

        # Set the payment method
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": request.data.get('cardNumber'),
                "exp_month": request.data.get('expirationMonth'),
                "exp_year": request.data.get('expirationYear'),
                "cvc": request.data.get('cvc')
            }
        )
        #
        # # Checks to see if customer exists, if not, creates it
        # customer_data = stripe.Customer.list(email=request.data.get('email')).data
        # if len(customer_data) == 0:
        #     customer = stripe.Customer.create(
        #         email=request.data.get('email'),
        #         payment_method=payment_method.get('id'),
        #     )
        #
        # else:
        #     customer = customer_data[0]
        #
        # # Create set up intent
        # setup_intent = stripe.SetupIntent.create(
        #     payment_method_types=["card"],
        #     payment_method=payment_method.get('id'),
        #     customer=customer.get('id')
        # )
        # print(setup_intent)
        # confirm_setup = stripe.SetupIntent.confirm(
        #     setup_intent.get('id'),
        #     payment_method=payment_method.get('id')
        # )
        # print(confirm_setup)
        # customer_data = stripe.Customer.list(email=request.data.get('email')).data
        # customer = customer_data[0]
        customer_data = stripe.Customer.list(email=request.data.get('email')).data
        customer = customer_data[0]
        intent = stripe.PaymentIntent.create(
            amount=5000,
            currency="usd",
            confirm=True,
            customer=customer,
            payment_method=payment_method
        )
        print(intent)

        return Response(status=status.HTTP_200_OK, data=customer)


class TestPayment(APIView):

    def post(self, request):
        client = StripeClient.objects.first()

        stripe.api_key = client.api_key
        test_payment_intent = stripe.PaymentIntent.create(
            amount=100,
            currency='usd',
            payment_method_types=['card'],
            receipt_email='ctcb57@gmail.com'
        )

        return Response(status=status.HTTP_200_OK, data=test_payment_intent)


class SaveStripeInfo(APIView):

    def post(self, request):
        data = request.data
        email = data['email']
        payment_method_id = data['payment_method_id']
        extra_message = ''

        customer_data = stripe.Customer.list(email=email).data

        if len(customer_data) == 0:
            customer = stripe.Customer.create(
                email=email,
                payment_method=payment_method_id
            )
        else:
            customer = customer_data[0]
            extra_message = "Customer already existed"

        response = {
            'message': 'Success',
            'data': {
                "customer_id": customer.id,
                "extra_message": extra_message
            }
        }
        return Response(status=status.HTTP_200_OK, data=response)


class CreateSetupIntent(APIView):

    def post(self, request):
        data = request.data
        email = data['email']

        message = ''
        customer_data = stripe.Customer.list(email=email).data

        if len(customer_data) == 0:
            customer = stripe.Customer.create(
                email=email
            )
            message = "Customer created"
        else:
            customer = customer_data[0]
            message = "Customer already existed"


        try:
            intent = stripe.SetupIntent.create(
                payment_method_types=["card"],
                customer=customer.get('id')
            )
            StripeSetupIntent.objects.create(
                stripe_customer=customer,
                stripe_setup_intent_id=intent.get('id')
            )
            message = "Setup intent created successfully"
            return Response(status=status.HTTP_201_CREATED, data={
                "message": message
            })
        except:
            message = "Processing Failed"
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": message
            })
