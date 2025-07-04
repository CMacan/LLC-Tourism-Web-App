# Generated by Django 5.1.4 on 2025-01-07 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='destination_images/')),
                ('category', models.CharField(choices=[('Beach', 'Beach'), ('Mountain', 'Mountain'), ('City', 'City'), ('Cultural', 'Cultural')], max_length=50)),
                ('rating', models.IntegerField()),
                ('popular', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('address', models.TextField()),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('cuisine_type', models.CharField(blank=True, max_length=100, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('price_range', models.CharField(blank=True, max_length=50, null=True)),
                ('opening_hours', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('menu_url', models.URLField(blank=True, null=True)),
                ('is_open', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='restaurant_photos/')),
            ],
        ),
    ]
