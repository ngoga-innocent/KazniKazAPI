# Generated by Django 3.2.20 on 2024-05-09 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('thumbnail', models.ImageField(upload_to='Category_thumbnails')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('color', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ShopModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('thumbnail', models.ImageField(upload_to='Shop_thumbnail')),
                ('location', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255, null=True)),
                ('like', models.IntegerField()),
                ('followers', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField(default=0)),
                ('thumbnail', models.ImageField(upload_to='product_thumbnail')),
                ('discount', models.IntegerField(null=True)),
                ('place', models.CharField(choices=[('Normal', 'Normal'), ('Vip', 'Vip')], default='Normal', max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(default='Other', on_delete=django.db.models.deletion.CASCADE, to='Product.category')),
                ('colors', models.ManyToManyField(related_name='product_colours', to='Product.Colors')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploader', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='Image_pictures')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='Product.productmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liker', to=settings.AUTH_USER_MODEL)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_liked', to='Product.shopmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.shopmodel')),
            ],
        ),
    ]
