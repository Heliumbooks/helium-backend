from django.urls import path

from helium_backend.slack.api import SlackWebhook

urlpatterns = [
    path('', SlackWebhook.as_view())
]