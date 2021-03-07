from slack_sdk import WebClient
from django.db import models
from django.urls import reverse


class SlackAccount(models.Model):
    token = models.TextField(default='', blank=True)

    class Meta:
        verbose_name_plural = "Accounts"

    def get_absolute_url(self):
        return reverse('slack-account-detail', kwargs={'pk': self.pk})

    def send_message(self, channel, message, bot_name=None, bot_image=None):
        client = WebClient(token=self.token)
        client.chat_postMessage(
            channel=channel.alt_id,
            text=message,
            username=bot_name if bot_name else channel.bot_name,
            icon_url=bot_image if bot_image else channel.bot_image,
            link_names=True
        )


class SlackChannel(models.Model):
    account = models.ForeignKey(SlackAccount, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    alt_id = models.CharField(max_length=50)
    bot_name = models.CharField(max_length=50, default='Channel Automator')
    bot_image = models.TextField(default='https://heliumbooks-webapp.s3.us-east-2.amazonaws.com/helium+primary+logo+(blue).png', blank=True)

    class Meta:
        verbose_name_plural = "Channels"
        ordering = ('name',)

    def send_message(self, message, bot_name=None, bot_image=None):
        if not bot_name:
            bot_name = self.bot_name
        if not bot_image:
            bot_image = self.bot_image
        print(bot_name)
        self.account.send_message(self, message, bot_name, bot_image)

    def __str__(self):
        return f"{self.name}"


class SlackUser(models.Model):
    account = models.ForeignKey(SlackAccount, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    alt_id = models.CharField(max_length=50)
    slack_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Users"
        ordering = ('name',)