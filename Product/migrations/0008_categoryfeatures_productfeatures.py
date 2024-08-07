# Generated by Django 3.2.20 on 2024-08-06 06:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0007_productmodel_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryFeatures',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.category')),
            ],
            options={
                'verbose_name': 'Features of Category',
                'verbose_name_plural': 'Features of Category',
            },
        ),
        migrations.CreateModel(
            name='ProductFeatures',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_features', to='Product.categoryfeatures')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_features', to='Product.productmodel')),
            ],
            options={
                'verbose_name': 'Features of Product',
            },
        ),
    ]
