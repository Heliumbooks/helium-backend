# Generated by Django 3.0.7 on 2022-02-21 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_book_book_ol_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='books.Subject'),
        ),
    ]
