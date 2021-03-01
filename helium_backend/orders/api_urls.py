from django.urls import path

from helium_backend.orders.api import OrderCreate
from helium_backend.orders.api import AllOrderList
from helium_backend.orders.api import OrderAddressSelection
from helium_backend.orders.api import OrderPickUpTimeSelection
from helium_backend.orders.api import CompleteOrderPlacement
from helium_backend.orders.api import PendingOrdersList
from helium_backend.orders.api import BookOrdersByOrderId
from helium_backend.orders.api import UpdateBookOrderStatus
from helium_backend.orders.api import UpdateBookOrderLibraryAssignment
from helium_backend.orders.api import UpdateBookOrderDueDate
from helium_backend.orders.api import AssignedBookOrdersByOrderId
from helium_backend.orders.api import ConfirmOrder
from helium_backend.orders.api import PendingLibraryPickUp
from helium_backend.orders.api import PendingLibraryPickUpById

urlpatterns = [
    path('all-orders/', AllOrderList.as_view()),
    path('pending-orders/', PendingOrdersList.as_view()),
    path('pending-orders/<int:pk>/confirm-availability/', BookOrdersByOrderId.as_view()),
    path('pending-orders/<int:pk>/confirm-due-date/', AssignedBookOrdersByOrderId.as_view()),
    path('pending-orders/<int:pk>/update-status/', UpdateBookOrderStatus.as_view()),
    path('pending-orders/<int:pk>/update-library/', UpdateBookOrderLibraryAssignment.as_view()),
    path('pending-orders/<int:pk>/update-due-date/', UpdateBookOrderDueDate.as_view()),
    path('pending-orders/<int:pk>/confirm-order/', ConfirmOrder.as_view()),
    path('pending-library-pickup/', PendingLibraryPickUp.as_view()),
    path('pending-library-pickup/<int:pk>/', PendingLibraryPickUpById.as_view()),
    path('create/', OrderCreate.as_view()),
    path('create/<int:pk>/address/', OrderAddressSelection.as_view()),
    path('create/<int:pk>/pickup-time/', OrderPickUpTimeSelection.as_view()),
    path('create/<int:pk>/payment/', CompleteOrderPlacement.as_view())
]
