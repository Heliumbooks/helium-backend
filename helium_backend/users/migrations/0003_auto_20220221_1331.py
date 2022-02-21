# Generated by Django 3.0.7 on 2022-02-21 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userpassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
