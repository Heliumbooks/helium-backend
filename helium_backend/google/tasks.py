from helium_backend.google.models import GoogleClient


def send_gmail_message(client_id, to, subject, message):
    client = GoogleClient.objects.get(pk=client_id)
    client.send_message(to, subject, message)
