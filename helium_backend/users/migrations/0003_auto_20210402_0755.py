# Generated by Django 3.0.7 on 2021-04-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userpassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contact_email_address',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='public_book_reviews',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='store_addresses',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='store_cards',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateField(blank=True, null=True),
        ),
    ]