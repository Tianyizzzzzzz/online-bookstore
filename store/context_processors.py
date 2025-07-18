"""
Context processors for the store app.

This module contains context processors that add data to all templates
automatically, such as cart item count and user-specific information.
"""

from .models import CartItem


def cart_item_count(request):
    """
    Add cart item count to template context.

    This context processor adds the number of items in the user's cart
    to every template context, allowing the cart badge to be displayed
    in the navigation bar.

    Args:
        request: The HTTP request object

    Returns:
        dict: Context dictionary with cart_item_count
    """

    if request.user.is_authenticated:
        try:
            # Get total quantity of items in cart
            cart_count = CartItem.objects.filter(user=request.user).count()
            return {'cart_item_count': cart_count}
        except:
            # If there's any error, return 0
            return {'cart_item_count': 0}
    else:
        # For anonymous users, cart count is 0
        return {'cart_item_count': 0}


def store_info(request):
    """
    Add store information to template context.

    This context processor adds general store information that
    might be useful across all templates.

    Args:
        request: The HTTP request object

    Returns:
        dict: Context dictionary with store information
    """

    return {
        'store_name': 'Online Bookstore',
        'store_tagline': 'Your Digital Library Awaits',
        'store_email': 'contact@onlinebookstore.com',
        'store_phone': '1-800-BOOKS-NOW',
        'store_address': '123 Library Street, Book City, BC 12345',
    }