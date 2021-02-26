from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import timedelta

from helium_backend.orders.models import Order
from helium_backend.orders.models import BookOrder, Status
from helium_backend.books.models import Book
from helium_backend.books.models import Author
from helium_backend.customers.models import Customer
from helium_backend.locations.models import Address, State, City
from helium_backend.libraries.models import Library

from helium_backend.stripe.tasks import create_customer, create_payment_method
from helium_backend.stripe.tasks import create_setup_intent


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
                emails=[request.data.get('email')]
            )

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
            return Response(status=status.HTTP_200_OK, data=order.id)

        else:
            order.drop_off_deadline = request.data.get('pickUpDateTime')
            order.save()
            return Response(status=status.HTTP_200_OK, data=order.id)


class CompleteOrderPlacement(APIView):
    permission_classes = (IsAuthenticated, )

    def patch(self, request, pk):
        current_time = timezone.now()

        try:
            order = Order.objects.filter(pk=pk).first()
            book_orders = BookOrder.objects.filter(order=order)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Didnt get order info")
        try:
            payment_method = create_payment_method(
                request.data.get('cardNumber'),
                request.data.get('expirationMonth'),
                request.data.get('expirationYear'),
                request.data.get('cvc')
            )
            print(payment_method)
            helium_stripe_customer = create_customer(
                request.data.get('email'),
                payment_method.get('id')
            )
            print(helium_stripe_customer)
            create_setup_intent(helium_stripe_customer)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Failed payment spot")

        try:
            order.payment_information_submitted = True
            order.completed_by_customer = True
            order.order_placed = current_time
            order.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="didnt save order info")

        try:
            for item in book_orders:
                item.status = "Order Placed"
                item.order_placed = current_time
                item.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="didnt save to book orders")

        return Response(status=status.HTTP_200_OK)


class PendingOrdersList(APIView):
    def get(self, request):
        current_time = timezone.now()
        orders = Order.objects.filter(payment_information_submitted=True, completed_by_customer=True,
                                      order_placed__lte=current_time, confirmed=False)\
            .values('id', 'customer__full_name', 'order_placed', 'drop_off_deadline').order_by('drop_off_deadline')
        return Response(orders)


class BookOrdersByOrderId(APIView):
    def get(self, request, pk):
        data = {"order_id": pk}
        book_orders = BookOrder.objects.filter(order_id=pk).values('id', 'title', 'author', 'order_placed', 'status',
                                                                   'pick_up_library_id', 'due_date')\
            .order_by('id')
        data['books'] = book_orders
        return Response(data)

    def patch(self, request, pk):
        order = Order.objects.filter(pk=pk).first()
        book_orders = request.data.get("books")
        for item in book_orders:
            book_order = BookOrder.objects.filter(pk=item.get('bookOrderId')).first()
            if not item.get('approved'):
                book_order.status = "Denied"
            else:
                book_order.status = "Awaiting Library Assignment"
            book_order.save()
            print(book_order.status)

        return Response(status=status.HTTP_200_OK, data=order.id)


class AssignedBookOrdersByOrderId(APIView):
    def get(self, request, pk):
        data = {"order_id": pk}
        book_orders = BookOrder.objects.filter(order_id=pk, status=Status.awaiting_library_pick_up.value)\
            .values('id', 'title', 'author', 'order_placed', 'status', 'pick_up_library_id', 'due_date') \
            .order_by('id')
        data['books'] = book_orders
        return Response(data)


class UpdateBookOrderStatus(APIView):
    def patch(self, request, pk):
        book_order = BookOrder.objects.filter(pk=pk).first()
        if request.data.get('approved'):
            book_order.status = "Awaiting Library Pick Up"
        else:
            book_order.status = "Denied"
        book_order.save()

        return Response(status=status.HTTP_200_OK)


class UpdateBookOrderLibraryAssignment(APIView):
    def patch(self, request, pk):
        book_order = BookOrder.objects.filter(pk=pk).first()
        try:
            library = Library.objects.filter(pk=request.data.get('libraryId')).first()
            book_order.pick_up_library = library
            book_order.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class UpdateBookOrderDueDate(APIView):
    def patch(self, request, pk):
        book_order = BookOrder.objects.filter(pk=pk).first()
        try:
            book_order.due_date = request.data.get('dueDate')
            book_order.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class ConfirmOrder(APIView):
    def patch(self, request, pk):
        order = Order.objects.filter(pk=pk).first()
        try:
            order.confirmed = True
            order.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)








