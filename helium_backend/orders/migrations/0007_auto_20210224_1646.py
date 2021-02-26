# Generated by Django 3.0.7 on 2021-02-24 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0002_library_active'),
        ('orders', '0006_order_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookorder',
            name='drop_off_library',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='drop_off_library', to='libraries.Library'),
        ),
        migrations.AddField(
            model_name='bookorder',
            name='pick_up_library',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pick_up_library', to='libraries.Library'),
        ),
    ]
