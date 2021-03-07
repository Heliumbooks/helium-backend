from django.utils import timezone

from helium_backend.slack.tasks import send_slack_message
from helium_backend.orders.models import Order, BookOrder, OrderStatus, Status
from helium_backend.slack.models import SlackChannel


def send_pending_order_notification(order_id):
    order = Order.objects.filter(pk=order_id).first()
    message = ""
    if order.customer:
        message += f"Customer: {order.customer.first_name} {order.customer.last_name} \n"
    books = BookOrder.objects.filter(order=order)
    message += "Books in order: \n"
    for item in books:
        message += f"{item.title} by {item.author}\n"
    message += f"Requested Dropoff Date: {order.drop_off_deadline.date()}\n"
    """
    Integrate true URL when complete
    """
    message += "URL"
    channel = SlackChannel.objects.first()
    bot_name = "New Book Order Request"

    send_slack_message(channel.id, message, bot_name)


def send_renewal_request_notification(order_id):
    order = Order.objects.filter(pk=order_id).first()
    message = ""
    if order.customer:
        message += f"Customer: {order.customer.first_name} {order.customer.last_name} requesting book renewal. \n"
    message += "Books: \n"
    books = BookOrder.objects.filter(status=Status.renewal_requested.value)
    for item in books:
        message += f"{item.title} by {item.author}\n"
        message += f"Due Date: {item.due_date}\n"
        """
        Integrate true URL when complete
        """
        message += "URL"
    channel = SlackChannel.objects.first()
    bot_name = "New Book Order Renewal Request"

    send_slack_message(channel.id, message, bot_name)


def daily_library_pickups():
    current_date = timezone.now().date()
    pending_order_pickups = Order.objects.filter(drop_off_deadline__date__lte=current_date,
                                           status=OrderStatus.confirmed.value)\
        .values('id', 'customer__first_name', 'customer__last_name', 'drop_off_address__street_address',
                'drop_off_address__city__name', 'drop_off_address__zip_code')
    if pending_order_pickups.count() < 1:
        message = f"No orders for library pick up for {current_date}"
        channel = SlackChannel.objects.first()
        send_slack_message(channel.id, message)
    message = f"Pending Library Pick-ups for {current_date}:\n\n"

    for order in pending_order_pickups:
        message += f"Customer: {order.get('customer__first_name')} {order.get('customer__last_name')}\n"
        message += f"Address: {order.get('drop_off_address__street_address')} " \
                   f"{order.get('drop_off_address__city__name')}, {order.get('drop_off_address__zip_code')}\n\n"

        message += "Books:\n"
        pending_book_order_pickups = BookOrder.objects.filter(order_id=order.get('id')).exclude(status=Status.denied.value)

        for book in pending_book_order_pickups:
            message += f"Book: {book.title} by {book.author}\n"
            message += f"Library: {book.pick_up_library.name}\n\n"

    """"
    Update when channels are created for Slack
    """
    channel = SlackChannel.objects.first()
    """
    Add Customer pickup logic
    """
    bot_name = "Daily Library Pickups"
    send_slack_message(channel.id, message, bot_name)


def daily_customer_pickups():
    current_date = timezone.now().date()
    pending_order_pickups = Order.objects.filter(pick_up_deadline__date=current_date,
                                                 status=OrderStatus.delivered_customer.value)\
        .values('id', 'customer__first_name', 'customer__last_name', 'pick_up_address__street_address',
                'pick_up_address__city__name', 'pick_up_address__zip_code')
    if pending_order_pickups.count() < 1:
        message = f"No orders for customer pick up for {current_date}"
        channel = SlackChannel.objects.first()
        send_slack_message(channel.id, message)
    else:
        message = f"Customer Returns Ready for Pick-up for {current_date}:\n\n"

        for order in pending_order_pickups:
            book_count = BookOrder.objects.filter(order_id=order.get('id')).exclude(status=Status.denied.value).count()
            message += f"Customer: {order.get('customer__first_name')} {order.get('customer__last_name')} - " \
                       f"{book_count} total Books\n"
            message += f"Address: {order.get('pick_up_address__street_address')} {order.get('pick_up_address__city__name')}, " \
                       f"{order.get('pick_up_address__zip_code')}"

        """
        Update when channels are created for Slack
        """
        channel = SlackChannel.objects.first()
        bot_name = "Daily Customer Pickups"
        send_slack_message(channel.id, message, bot_name)


def daily_overdue_books():
    current_date = timezone.now().date()
    overdue_books = BookOrder.objects.filter(due_date__lte=current_date)\
        .values('id', 'order__customer__first_name', 'order__customer__last_name', 'title', 'author', 'due_date',
                'order__customer_id')\
        .order_by('order__customer_id')
    if overdue_books.count() < 1:
        message = f"No overdue books as of {current_date}"
        channel = SlackChannel.objects.first()
        send_slack_message(channel.id, message, bot_name="Daily Overdue Report")
    else:
        message = f"The following orders are currently overdue:\n\n"
        for item in overdue_books:
            message += f"Customer: {item.get('order__customer__first_name')} {item.get('order__customer_last_name')}\n" \
                       f"Book: {item.get('title')} by {item.get('author')}\n" \
                        f"Due Date: {item.get('due_date')}\n\n"
        """
        Update when channels are created for Slack
        """
        channel = SlackChannel.objects.first()
        bot_name = "Daily Overdue Report"
        send_slack_message(channel.id, message, bot_name)


def daily_book_report():
    pass



