# Generated by Django 3.0.7 on 2021-02-05 02:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('full_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('phone_numbers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='', max_length=20), default=list, size=None)),
                ('emails', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='', max_length=200), default=list, size=None)),
                ('orders', models.IntegerField(default=0)),
                ('referrals', models.IntegerField(default=0)),
                ('referral_code', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('referred_by_code', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
            options={
                'ordering': ('full_name',),
            },
        ),
    ]
