from django.contrib import admin
from helium_backend.slack.models import SlackAccount
from helium_backend.slack.models import SlackChannel
from helium_backend.slack.models import SlackUser


admin.site.register(SlackAccount)
admin.site.register(SlackChannel)
admin.site.register(SlackUser)
