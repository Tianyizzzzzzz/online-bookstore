"""
Models for the online bookstore application (without image fields).

This module contains all the database models for managing books,
shopping cart, orders, and user data.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal


class Book(models.Model):
    """
    Model representing a book in the bookstore.

    Contains all the essential information about a book including
    title, author, pricing, and inventory management.
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Book Title",
        help_text="The complete title of the book"
    )

    author = models.CharField(
        max_length=100,
        verbose_name="Author Name",
        help_text="The author(s) of the book"
    )

    isbn = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="ISBN",
        help_text="International Standard Book Number (10 or 13 digits)"
    )

    description = models.TextField(
        verbose_name="Book Description",
        help_text="Detailed description of the book content"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Price ($)",
        help_text="Book price in USD"
    )

    stock_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock Quantity",
        help_text="Number of books available in inventory"
    )

    cover_image = models.ImageField(
        upload_to='books/covers/',
        null=True,
        blank=True,
        verbose_name="Book Cover Image",
        help_text="Upload book cover image"
    )

    placeholder_pdf = models.FileField(
        upload_to='books/pdfs/',
        null=True,
        blank=True,
        verbose_name="eBook PDF File",
        help_text="PDF file to be sent as eBook placeholder"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Added"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="Featured Book",
        help_text="Mark this book as featured on homepage"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def is_in_stock(self):
        """Check if book is available in stock"""
        return self.stock_quantity > 0

    @property
    def average_rating(self):
        """Calculate average rating (placeholder for future feature)"""
        return 0  # TODO: Implement when review system is added


class CartItem(models.Model):
    """
    Model representing items in a user's shopping cart.

    Links users to books they want to purchase with quantity information.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Customer",
        help_text="The user who added this item to cart"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Book",
        help_text="The book added to cart"
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        verbose_name="Quantity",
        help_text="Number of copies"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Added to Cart"
    )

    class Meta:
        unique_together = ('user', 'book')
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.user.username} - {self.book.title} (x{self.quantity})"

    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return self.book.price * self.quantity


class Order(models.Model):
    """
    Model representing a customer's order.

    Contains order information including customer details,
    order status, and total amount.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Customer",
        help_text="The customer who placed this order"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Total Amount ($)",
        help_text="Total order amount in USD"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Order Status",
        help_text="Current status of the order"
    )

    # Shipping Information
    shipping_address = models.TextField(
        verbose_name="Shipping Address",
        help_text="Complete shipping address"
    )

    shipping_city = models.CharField(
        max_length=100,
        verbose_name="City"
    )

    shipping_state = models.CharField(
        max_length=100,
        verbose_name="State/Province"
    )

    shipping_zip_code = models.CharField(
        max_length=20,
        verbose_name="ZIP/Postal Code"
    )

    shipping_country = models.CharField(
        max_length=100,
        default="United States",
        verbose_name="Country"
    )

    # Order Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Order Date"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )

    # Email tracking
    email_sent = models.BooleanField(
        default=False,
        verbose_name="Email Sent",
        help_text="Whether confirmation email has been sent"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - ${self.total_amount}"

    @property
    def order_number(self):
        """Generate a formatted order number"""
        return f"ORD-{self.id:06d}"


class OrderItem(models.Model):
    """
    Model representing individual items within an order.

    This is a through model that connects orders to books
    with quantity and pricing information at the time of purchase.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Order",
        help_text="The order this item belongs to"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Book",
        help_text="The book purchased"
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Quantity",
        help_text="Number of copies purchased"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Unit Price ($)",
        help_text="Price per book at time of purchase"
    )

    class Meta:
        unique_together = ('order', 'book')
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.order.order_number} - {self.book.title} (x{self.quantity})"

    @property
    def total_price(self):
        """Calculate total price for this order item"""
        return self.price * self.quantity


class UserProfile(models.Model):
    """
    Extended user profile model.

    Stores additional user information beyond Django's default User model.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="User"
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Phone Number",
        help_text="Contact phone number"
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of Birth"
    )

    # Default shipping address
    default_shipping_address = models.TextField(
        blank=True,
        verbose_name="Default Shipping Address"
    )

    default_shipping_city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Default City"
    )

    default_shipping_state = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Default State"
    )

    default_shipping_zip = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Default ZIP Code"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Profile Created"
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile"