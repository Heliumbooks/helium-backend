# Generated by Django 3.0.7 on 2021-02-24 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20210223_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]