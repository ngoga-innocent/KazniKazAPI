# Generated by Django 3.2.20 on 2024-08-17 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0016_auto_20240815_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopmodel',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='Shop_thumbnail'),
        ),
    ]
