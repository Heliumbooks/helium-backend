import base64
from email.mime.text import MIMEText
from django.db import models
from google.oauth2 import service_account
from apiclient import errors

from googleapiclient.discovery import build


class GoogleClient(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.address

    def create_message(self, sender, to, subject, message_text):
        message = MIMEText(message_text, 'html')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_message(self, to, subject, message):
        """Send an email message.
        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.
        Returns:
          Sent Message.
        """
        service = self.service_account_email_login()
        message = message.replace('\n', '<br />')
        message = self.create_message(f"{self.name} <{self.address}>", to, subject, message)

        try:
            message = (service.users().messages().send(userId='me', body=message)
                       .execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def service_account_email_login(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        SERVICE_ACCOUNT_FILE = 'service-key.json'

        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        delegated_credentials = credentials.with_subject(self.address)
        service = build('gmail', 'v1', credentials=delegated_credentials)

        # credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject="mike.haydon@stayfrontdesk.com")
        # service = build('admin', 'directory_v1', credentials=credentials)

        return service