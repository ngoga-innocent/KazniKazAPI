# Generated by Django 3.2.20 on 2024-05-14 08:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Wallet', '0002_alter_mywallet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallethistory',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
