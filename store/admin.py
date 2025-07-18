"""
Django admin configuration for the store app.

This module customizes the Django admin interface for managing
books, orders, and other bookstore data.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Book, CartItem, Order, OrderItem, UserProfile


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Book model.

    Provides comprehensive management interface for books including
    search, filtering, and bulk actions.
    """

    list_display = [
        'title', 'author', 'price', 'stock_quantity',
        'is_featured', 'created_at', 'cover_image_preview'
    ]

    list_filter = [
        'is_featured', 'created_at', 'stock_quantity'
    ]

    search_fields = [
        'title', 'author', 'isbn', 'description'
    ]

    list_editable = [
        'price', 'stock_quantity', 'is_featured'
    ]

    readonly_fields = [
        'created_at', 'updated_at', 'cover_image_preview'
    ]

    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'isbn', 'description')
        }),
        ('Pricing and Inventory', {
            'fields': ('price', 'stock_quantity', 'is_featured')
        }),
        ('Media Files', {
            'fields': ('cover_image', 'cover_image_preview', 'placeholder_pdf')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Custom actions
    actions = ['mark_as_featured', 'mark_as_not_featured', 'update_stock']

    def cover_image_preview(self, obj):
        """Display thumbnail of book cover in admin"""
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 70px; object-fit: cover;" />',
                obj.cover_image.url
            )
        return "No image"

    cover_image_preview.short_description = "Cover Preview"

    def mark_as_featured(self, request, queryset):
        """Mark selected books as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(
            request,
            f'{updated} books were successfully marked as featured.'
        )

    mark_as_featured.short_description = "Mark selected books as featured"

    def mark_as_not_featured(self, request, queryset):
        """Remove featured status from selected books"""
        updated = queryset.update(is_featured=False)
        self.message_user(
            request,
            f'{updated} books were successfully unmarked as featured.'
        )

    mark_as_not_featured.short_description = "Remove featured status"

    def update_stock(self, request, queryset):
        """Custom action to update stock - redirects to change form"""
        # This is a placeholder - in real implementation, you might want
        # a custom form for bulk stock updates
        pass

    update_stock.short_description = "Update stock quantities"


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for OrderItem model.

    Allows editing order items directly within the order admin page.
    """

    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

    def total_price(self, obj):
        """Calculate total price for the order item"""
        return f"${obj.total_price:.2f}"

    total_price.short_description = "Total Price"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model.

    Provides comprehensive order management with inline order items.
    """

    list_display = [
        'order_number', 'user', 'total_amount', 'status',
        'created_at', 'email_sent', 'order_items_count'
    ]

    list_filter = [
        'status', 'created_at', 'email_sent', 'shipping_country'
    ]

    search_fields = [
        'user__username', 'user__email', 'user__first_name',
        'user__last_name', 'shipping_city', 'shipping_state'
    ]

    list_editable = ['status']

    readonly_fields = [
        'order_number', 'created_at', 'updated_at', 'total_amount'
    ]

    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'total_amount', 'status', 'email_sent')
        }),
        ('Shipping Information', {
            'fields': (
                'shipping_address', 'shipping_city', 'shipping_state',
                'shipping_zip_code', 'shipping_country'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Custom actions
    actions = ['mark_as_completed', 'mark_as_shipped', 'resend_confirmation_email']

    def order_items_count(self, obj):
        """Display number of items in the order"""
        return obj.items.count()

    order_items_count.short_description = "Items Count"

    def mark_as_completed(self, request, queryset):
        """Mark selected orders as completed"""
        updated = queryset.update(status='completed')
        self.message_user(
            request,
            f'{updated} orders were successfully marked as completed.'
        )

    mark_as_completed.short_description = "Mark selected orders as completed"

    def mark_as_shipped(self, request, queryset):
        """Mark selected orders as shipped"""
        updated = queryset.update(status='shipped')
        self.message_user(
            request,
            f'{updated} orders were successfully marked as shipped.'
        )

    mark_as_shipped.short_description = "Mark selected orders as shipped"

    def resend_confirmation_email(self, request, queryset):
        """Resend confirmation email for selected orders"""
        from .views import send_order_confirmation_email

        count = 0
        for order in queryset:
            try:
                send_order_confirmation_email(order)
                count += 1
            except Exception as e:
                self.message_user(
                    request,
                    f'Error sending email for order {order.order_number}: {str(e)}',
                    level='ERROR'
                )

        if count > 0:
            self.message_user(
                request,
                f'Successfully resent confirmation emails for {count} orders.'
            )

    resend_confirmation_email.short_description = "Resend confirmation emails"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for CartItem model.

    Provides interface to view and manage shopping cart items.
    """

    list_display = ['user', 'book', 'quantity', 'total_price', 'created_at']
    list_filter = ['created_at', 'book__author']
    search_fields = ['user__username', 'book__title', 'book__author']
    readonly_fields = ['total_price', 'created_at']

    def total_price(self, obj):
        """Display total price for the cart item"""
        return f"${obj.total_price:.2f}"

    total_price.short_description = "Total Price"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.

    Provides interface to manage extended user information.
    """

    list_display = [
        'user', 'phone_number', 'default_shipping_city',
        'default_shipping_state', 'created_at'
    ]

    search_fields = [
        'user__username', 'user__email', 'user__first_name',
        'user__last_name', 'phone_number'
    ]

    list_filter = [
        'created_at', 'default_shipping_state', 'default_shipping_city'
    ]

    readonly_fields = ['created_at']

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number', 'date_of_birth')
        }),
        ('Default Shipping Address', {
            'fields': (
                'default_shipping_address', 'default_shipping_city',
                'default_shipping_state', 'default_shipping_zip'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# Register OrderItem separately if needed for direct access
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for OrderItem model.

    Provides interface to view individual order items.
    """

    list_display = ['order', 'book', 'quantity', 'price', 'total_price']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['order__user__username', 'book__title', 'book__author']
    readonly_fields = ['total_price']

    def total_price(self, obj):
        """Display total price for the order item"""
        return f"${obj.total_price:.2f}"

    total_price.short_description = "Total Price"

    def has_add_permission(self, request):
        """Disable adding order items directly"""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable changing order items directly"""
        return False


# Customize admin site
admin.site.empty_value_display = '(None)'
