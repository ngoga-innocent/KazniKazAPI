# Generated by Django 3.2.20 on 2024-07-25 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0006_alter_device_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='signup_type',
            field=models.CharField(default='none', max_length=50),
        ),
    ]