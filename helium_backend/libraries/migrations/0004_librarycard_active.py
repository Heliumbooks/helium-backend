# Generated by Django 3.0.7 on 2021-03-03 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0003_librarycard'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarycard',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]