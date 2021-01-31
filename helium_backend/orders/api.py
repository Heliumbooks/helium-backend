from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone

from helium_backend.orders.models import Order
from helium_backend.orders.models import BookOrder
from helium_backend.books.models import Book
from helium_backend.books.models import Author
from helium_backend.customers.models import Customer


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
