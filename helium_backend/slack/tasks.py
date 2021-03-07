from helium_backend.slack.models import SlackChannel


def send_slack_message(channel_id, message, bot_name="", bot_image=""):
    channel = SlackChannel.objects.get(pk=channel_id)
    if bot_name:
        channel.bot_name = bot_name
    if bot_image:
        channel.bot_image = bot_image
    channel.send_message(message)
