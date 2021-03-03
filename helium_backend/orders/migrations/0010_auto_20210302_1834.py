# Generated by Django 3.0.7 on 2021-03-03 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0003_librarycard'),
        ('orders', '0009_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookorder',
            name='library_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='libraries.LibraryCard'),
        ),
        migrations.AlterField(
            model_name='bookorder',
            name='status',
            field=models.CharField(blank=True, choices=[('Incomplete', 'Incomplete'), ('Order Placed', 'Placed'), ('Awaiting Library Assignment', 'Awaiting_Library_Assignment'), ('Awaiting Library Pick Up', 'Awaiting_Library_Pick_Up'), ('Awaiting Delivery', 'Awaiting_Delivery'), ('Awaiting Customer Pick Up', 'Awaiting_Customer_Pick_Up'), ('Awaiting Library Return', 'Awaiting_Library_Return'), ('Delivered', 'Delivered'), ('Completed', 'Completed'), ('Denied', 'Denied'), ('Overdue', 'Overdue'), ('Lost', 'Lost')], default='', max_length=100, null=True),
        ),
    ]
