from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import timedelta

from helium_backend.orders.models import Order
from helium_backend.orders.models import BookOrder
from helium_backend.books.models import Book
from helium_backend.books.models import Author
from helium_backend.customers.models import Customer
from helium_backend.locations.models import Address, State, City


class AllOrderList(APIView):
    def get(self, request):
        orders = Order.objects.all().values('id', 'customer__full_name', 'order_placed').order_by('order_placed')
        return Response(orders)


class OrderCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        current_time = timezone.now()
        user = request.user

        if len(request.data.get('requestedBooks')) > 0:
            customer, customer_created = Customer.objects.get_or_create(
                full_name=user.full_name,
                first_name=user.first_name,
                last_name=user.last_name,
                user=user,
            )
            print(customer)

            order = Order.objects.create(
                customer=customer,
                order_initiated=current_time,
                completed_by_customer=False
            )
            for item in request.data.get('requestedBooks'):
                if item.get('title') and item.get('author'):
                    converted_author_name = item.get("author").split(" ", 1)
                    author, author_created = Author.objects.get_or_create(
                        first_name=converted_author_name[0],
                        last_name=converted_author_name[1],
                        full_name=item.get("author")
                    )

                    book, book_created = Book.objects.get_or_create(
                        title=item.get('title'),
                        author=author,
                    )

                    BookOrder.objects.create(
                        order=order,
                        book=book,
                        title=item.get('title'),
                        author=item.get('author'),
                        status="Incomplete"
                    )
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_200_OK, data=order.id)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderAddressSelection(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        user = request.user
        if not request.data.get('streetAddress'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('state') != "WI" and request.data.get('state').lower() != "wisconsin":
            error_message = {"message": "Unable to place orders outside of Wisconsin"}
            return Response(status=status.HTTP_403_FORBIDDEN, data=error_message)

        try:
            order = Order.objects.filter(pk=pk).first()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        state = State.objects.filter(name="Wisconsin", abbreviation="WI").first()

        city, city_created = City.objects.get_or_create(
            name=request.data.get('city'),
            timezone="America/Chicago",
            state=state
        )

        """To Do: Write some code that calculates the longitude and latitude of the address using Google"""

        address, address_created = Address.objects.get_or_create(
            customer=user,
            street_address=request.data.get('streetAddress'),
            additional_street_address=request.data.get('additionalStreetAddress'),
            city=city,
            zip_code=request.data.get('zipCode'),
            type="Delivery",
            longitude=0,
            latitude=0
        )

        try:
            order.drop_off_location = request.data.get('dropOffLocation')
            order.address = address
            order.save()
            return Response(status=status.HTTP_200_OK, data=order.id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderPickUpTimeSelection(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        try:
            order = Order.objects.filter(pk=pk).first()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        current_time = timezone.now()
        cutoff_date_time = current_time.replace(hour=16, minute=0, second=0)

        if not request.data.get('pickUpTime') and not request.data.get('pickUpDate'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('pickUpDate') == current_time.date() \
                and (request.data.get('pickUpDateTime') + timedelta(hours=6)) > cutoff_date_time:
            error_message = {"error": "Time requested is after delivery cutoff time"}
            return Response(status=status.HTTP_403_FORBIDDEN, data=error_message)

        if request.data.get('asap'):
            order.drop_off_deadline = timezone.now() + timedelta(days=2)
            order.save()
            return Response(status=status.HTTP_200_OK)

        else:
            order.drop_off_deadline = request.data.get('pickUpDateTime')
            order.save()
            return Response(status=status.HTTP_200_OK)


class CompleteOrderPlacement(APIView):
    permission_classes = (IsAuthenticated, )

    def patch(self, request, pk):
        current_time = timezone.now()

        try:
            order = Order.objects.filter(pk=pk).first()
            book_orders = BookOrder.objects.filter(order=order)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        """
        Need to add the processing of the stripe payment here
        """
        try:
            order.payment_information_submitted = True
            order.completed_by_customer = True
            order.order_placed = current_time
            order.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            for item in book_orders:
                item.status = "Order Placed"
                item.order_placed = current_time
                item.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

