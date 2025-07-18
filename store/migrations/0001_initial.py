# Generated by Django 4.2.7 on 2025-07-18 02:40

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='The complete title of the book', max_length=200, verbose_name='Book Title')),
                ('author', models.CharField(help_text='The author(s) of the book', max_length=100, verbose_name='Author Name')),
                ('isbn', models.CharField(help_text='International Standard Book Number (10 or 13 digits)', max_length=13, unique=True, verbose_name='ISBN')),
                ('description', models.TextField(help_text='Detailed description of the book content', verbose_name='Book Description')),
                ('price', models.DecimalField(decimal_places=2, help_text='Book price in USD', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Price ($)')),
                ('stock_quantity', models.PositiveIntegerField(default=0, help_text='Number of books available in inventory', verbose_name='Stock Quantity')),
                ('cover_image_url', models.URLField(blank=True, help_text='URL to book cover image', null=True, verbose_name='Book Cover Image URL')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('is_featured', models.BooleanField(default=False, help_text='Mark this book as featured on homepage', verbose_name='Featured Book')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, help_text='Total order amount in USD', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Total Amount ($)')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', help_text='Current status of the order', max_length=20, verbose_name='Order Status')),
                ('shipping_address', models.TextField(help_text='Complete shipping address', verbose_name='Shipping Address')),
                ('shipping_city', models.CharField(max_length=100, verbose_name='City')),
                ('shipping_state', models.CharField(max_length=100, verbose_name='State/Province')),
                ('shipping_zip_code', models.CharField(max_length=20, verbose_name='ZIP/Postal Code')),
                ('shipping_country', models.CharField(default='United States', max_length=100, verbose_name='Country')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Order Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('email_sent', models.BooleanField(default=False, help_text='Whether confirmation email has been sent', verbose_name='Email Sent')),
                ('user', models.ForeignKey(help_text='The customer who placed this order', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, help_text='Contact phone number', max_length=20, verbose_name='Phone Number')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('default_shipping_address', models.TextField(blank=True, verbose_name='Default Shipping Address')),
                ('default_shipping_city', models.CharField(blank=True, max_length=100, verbose_name='Default City')),
                ('default_shipping_state', models.CharField(blank=True, max_length=100, verbose_name='Default State')),
                ('default_shipping_zip', models.CharField(blank=True, max_length=20, verbose_name='Default ZIP Code')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Profile Created')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(help_text='Number of copies purchased', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantity')),
                ('price', models.DecimalField(decimal_places=2, help_text='Price per book at time of purchase', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Unit Price ($)')),
                ('book', models.ForeignKey(help_text='The book purchased', on_delete=django.db.models.deletion.CASCADE, to='store.book', verbose_name='Book')),
                ('order', models.ForeignKey(help_text='The order this item belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
                'unique_together': {('order', 'book')},
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, help_text='Number of copies', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Quantity')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Added to Cart')),
                ('book', models.ForeignKey(help_text='The book added to cart', on_delete=django.db.models.deletion.CASCADE, to='store.book', verbose_name='Book')),
                ('user', models.ForeignKey(help_text='The user who added this item to cart', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
                'unique_together': {('user', 'book')},
            },
        ),
    ]
