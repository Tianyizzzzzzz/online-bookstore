"""
URL configuration for the store app.

This module defines all the URL patterns for the bookstore application,
mapping URLs to their corresponding view functions.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Define URL patterns for the store app
urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),

    # Book-related URLs
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('search/', views.search_books_ajax, name='search_books_ajax'),

    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='store/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='store/password_reset.html',
        subject_template_name='store/email/password_reset_subject.txt',
        email_template_name='store/email/password_reset_email.html',
        success_url='/password-reset-done/'
    ), name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='store/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='store/password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='store/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Shopping cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout and order URLs
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation_view, name='order_confirmation'),
    path('order-history/', views.order_history_view, name='order_history'),

    # User profile URLs
    path('profile/', views.profile_view, name='profile'),

    # Additional utility URLs (can be expanded)
    path('about/', views.home_view, name='about'),  # Placeholder
    path('contact/', views.home_view, name='contact'),  # Placeholder
]
