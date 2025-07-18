"""
Views for the online bookstore application.

This module contains all the view functions and classes that handle
HTTP requests and return appropriate responses.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.db import transaction
from decimal import Decimal
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import Book, CartItem, Order, OrderItem, UserProfile
from .forms import (
    CustomUserCreationForm, AddToCartForm, UpdateCartForm,
    CheckoutForm, BookSearchForm, UserProfileForm
)


class BookListView(ListView):
    """
    Display list of books with search and filtering functionality.

    Supports pagination, search by title/author, and sorting options.
    """

    model = Book
    template_name = 'store/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        """Filter and sort books based on search parameters"""
        queryset = Book.objects.filter(stock_quantity__gt=0)

        # Get search parameters
        query = self.request.GET.get('query')
        category = self.request.GET.get('category')
        sort_by = self.request.GET.get('sort_by', '-created_at')

        # Apply search filter
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(description__icontains=query)
            )

        # Apply category filter (placeholder for future implementation)
        if category and category != 'all':
            # TODO: Add category field to Book model
            pass

        # Apply sorting
        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        """Add search form and current parameters to context"""
        context = super().get_context_data(**kwargs)
        context['search_form'] = BookSearchForm(self.request.GET)
        context['current_query'] = self.request.GET.get('query', '')
        context['current_category'] = self.request.GET.get('category', 'all')
        context['current_sort'] = self.request.GET.get('sort_by', '-created_at')
        context['featured_books'] = Book.objects.filter(
            is_featured=True,
            stock_quantity__gt=0
        )[:3]
        return context


class BookDetailView(DetailView):
    """
    Display detailed information about a specific book.

    Shows book details and provides add to cart functionality.
    """

    model = Book
    template_name = 'store/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        """Add add to cart form to context"""
        context = super().get_context_data(**kwargs)
        context['add_to_cart_form'] = AddToCartForm()

        # Get related books (same author or similar title)
        book = self.get_object()
        related_books = Book.objects.filter(
            Q(author=book.author) | Q(title__icontains=book.title.split()[0])
        ).exclude(id=book.id).filter(stock_quantity__gt=0)[:4]

        context['related_books'] = related_books
        return context


def register_view(request):
    """
    Handle user registration.

    Creates new user account and redirects to login page.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f'Account created successfully for {user.username}! You can now log in.'
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'store/register.html', {'form': form})


@login_required
def add_to_cart(request, book_id):
    """
    Add a book to the user's shopping cart.

    Handles both new additions and quantity updates for existing items.
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            # Check if there's enough stock
            if quantity > book.stock_quantity:
                messages.error(
                    request,
                    f'Sorry, only {book.stock_quantity} copies of "{book.title}" are available.'
                )
                return redirect('book_detail', pk=book_id)

            # Get or create cart item
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                book=book,
                defaults={'quantity': quantity}
            )

            if not created:
                # Update existing cart item
                new_quantity = cart_item.quantity + quantity
                if new_quantity > book.stock_quantity:
                    messages.error(
                        request,
                        f'Cannot add {quantity} more copies. Only {book.stock_quantity} available.'
                    )
                    return redirect('book_detail', pk=book_id)

                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(
                    request,
                    f'Updated "{book.title}" quantity to {cart_item.quantity} in your cart.'
                )
            else:
                messages.success(
                    request,
                    f'Added "{book.title}" to your cart.'
                )

            return redirect('cart')

    return redirect('book_detail', pk=book_id)


@login_required
def cart_view(request):
    """
    Display the user's shopping cart.

    Shows all items in cart with quantity update and removal options.
    """
    cart_items = CartItem.objects.filter(user=request.user).select_related('book')

    # Calculate total
    total_amount = sum(item.total_price for item in cart_items)

    # Handle quantity updates
    if request.method == 'POST' and 'update_cart' in request.POST:
        for item in cart_items:
            quantity_key = f'quantity_{item.id}'
            if quantity_key in request.POST:
                try:
                    new_quantity = int(request.POST[quantity_key])
                    if new_quantity > 0 and new_quantity <= item.book.stock_quantity:
                        item.quantity = new_quantity
                        item.save()
                    elif new_quantity > item.book.stock_quantity:
                        messages.error(
                            request,
                            f'Only {item.book.stock_quantity} copies of "{item.book.title}" available.'
                        )
                except (ValueError, TypeError):
                    pass

        return redirect('cart')

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }

    return render(request, 'store/cart.html', context)


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """
    Remove an item from the shopping cart.

    Deletes the cart item and redirects back to cart page.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    book_title = cart_item.book.title
    cart_item.delete()

    messages.success(request, f'Removed "{book_title}" from your cart.')
    return redirect('cart')


@login_required
def checkout_view(request):
    """
    Handle the checkout process.

    Collects shipping information and creates order.
    """
    cart_items = CartItem.objects.filter(user=request.user).select_related('book')

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    # Calculate total
    total_amount = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            # Create order with transaction to ensure data consistency
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = total_amount
                order.save()

                # Create order items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        book=cart_item.book,
                        quantity=cart_item.quantity,
                        price=cart_item.book.price
                    )

                    # Update book stock
                    book = cart_item.book
                    book.stock_quantity -= cart_item.quantity
                    book.save()

                # Clear cart
                cart_items.delete()

                # Send confirmation email
                send_order_confirmation_email(order)

                messages.success(
                    request,
                    f'Order #{order.order_number} placed successfully!'
                )
                return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm(user=request.user)

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_amount': total_amount,
    }

    return render(request, 'store/checkout.html', context)


@login_required
def order_confirmation_view(request, order_id):
    """
    Display order confirmation page.

    Shows order details and confirmation message.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order,
    }

    return render(request, 'store/order_confirmation.html', context)


@login_required
def order_history_view(request):
    """
    Display user's order history.

    Shows all orders placed by the current user.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,
    }

    return render(request, 'store/order_history.html', context)


@login_required
def profile_view(request):
    """
    Display and update user profile.

    Allows users to view and modify their profile information.
    """
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)

    context = {
        'form': form,
        'profile': profile,
    }

    return render(request, 'store/profile.html', context)


def send_order_confirmation_email(order):
    """
    Send order confirmation email with eBook attachments.

    Creates and sends email with PDF files for purchased books.
    """
    try:
        # Create email subject and body
        subject = f'Order Confirmation - {order.order_number}'

        # Render email template
        html_message = render_to_string('store/email/order_confirmation.html', {
            'order': order,
            'user': order.user,
        })

        # Create email message
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[order.user.email],
        )
        email.content_subtype = 'html'

        # Attach PDF files for each book
        for order_item in order.items.all():
            book = order_item.book

            # If book has a placeholder PDF, attach it
            if book.placeholder_pdf:
                try:
                    email.attach_file(book.placeholder_pdf.path)
                except:
                    # If PDF file doesn't exist, create a placeholder
                    create_placeholder_pdf(email, book, order_item.quantity)
            else:
                # Create a placeholder PDF
                create_placeholder_pdf(email, book, order_item.quantity)

        # Send email
        email.send()

        # Mark email as sent
        order.email_sent = True
        order.save()

    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"Error sending email: {str(e)}")


def create_placeholder_pdf(email, book, quantity):
    """
    Create a placeholder PDF file for eBook delivery.

    Generates a simple PDF with book information.
    """
    # Create PDF in memory
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Add content to PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, f"eBook: {book.title}")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 720, f"Author: {book.author}")
    pdf.drawString(100, 700, f"ISBN: {book.isbn}")
    pdf.drawString(100, 680, f"Quantity: {quantity}")

    pdf.drawString(100, 640, "Thank you for your purchase!")
    pdf.drawString(100, 620, "This is a placeholder PDF file.")
    pdf.drawString(100, 600, "In a real bookstore, this would be the actual eBook.")

    pdf.drawString(100, 560, "Book Description:")

    # Add description with line wrapping
    description = book.description
    lines = []
    words = description.split()
    current_line = ""

    for word in words:
        if len(current_line + word) < 70:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    y_position = 540
    for line in lines[:10]:  # Limit to 10 lines
        pdf.drawString(100, y_position, line)
        y_position -= 20

    pdf.save()

    # Attach to email
    buffer.seek(0)
    email.attach(
        f"{book.title.replace(' ', '_')}_ebook.pdf",
        buffer.read(),
        'application/pdf'
    )
    buffer.close()


def home_view(request):
    """
    Display the home page.

    Shows featured books and recent additions.
    """
    featured_books = Book.objects.filter(
        is_featured=True,
        stock_quantity__gt=0
    )[:6]

    recent_books = Book.objects.filter(
        stock_quantity__gt=0
    ).order_by('-created_at')[:8]

    context = {
        'featured_books': featured_books,
        'recent_books': recent_books,
    }

    return render(request, 'store/home.html', context)


def search_books_ajax(request):
    """
    AJAX endpoint for book search autocomplete.

    Returns JSON response with matching book titles.
    """
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        if query:
            books = Book.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )[:10]

            results = []
            for book in books:
                results.append({
                    'id': book.id,
                    'title': book.title,
                    'author': book.author,
                    'price': str(book.price),
                })

            return JsonResponse({'results': results})

    return JsonResponse({'results': []})