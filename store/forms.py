"""
Forms for the online bookstore application.

This module contains all the forms used for user input validation
and rendering in the bookstore application.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Order, UserProfile


class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form with additional fields.

    Includes email validation and additional user information.
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        }),
        help_text='Required. Enter a valid email address.'
    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        """Save user with additional fields"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        return user


class AddToCartForm(forms.Form):
    """
    Form for adding books to shopping cart.

    Allows users to specify quantity when adding items to cart.
    """

    quantity = forms.IntegerField(
        min_value=1,
        max_value=99,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px;',
            'min': '1',
            'max': '99'
        }),
        help_text='Select quantity (1-99)'
    )


class UpdateCartForm(forms.Form):
    """
    Form for updating cart item quantities.

    Used in the shopping cart page to allow quantity modifications.
    """

    quantity = forms.IntegerField(
        min_value=1,
        max_value=99,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'style': 'width: 70px;',
            'min': '1',
            'max': '99'
        })
    )


class CheckoutForm(forms.ModelForm):
    """
    Form for order checkout process.

    Collects shipping information and validates order details.
    """

    class Meta:
        model = Order
        fields = [
            'shipping_address',
            'shipping_city',
            'shipping_state',
            'shipping_zip_code',
            'shipping_country'
        ]
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your complete shipping address'
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'shipping_state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'shipping_zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ZIP/Postal Code'
            }),
            'shipping_country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Pre-fill form with user's default shipping info if available
        if user and hasattr(user, 'profile'):
            profile = user.profile
            if profile.default_shipping_address:
                self.fields['shipping_address'].initial = profile.default_shipping_address
            if profile.default_shipping_city:
                self.fields['shipping_city'].initial = profile.default_shipping_city
            if profile.default_shipping_state:
                self.fields['shipping_state'].initial = profile.default_shipping_state
            if profile.default_shipping_zip:
                self.fields['shipping_zip_code'].initial = profile.default_shipping_zip

    def clean_shipping_zip_code(self):
        """Validate ZIP code format"""
        zip_code = self.cleaned_data.get('shipping_zip_code')
        if zip_code:
            # Basic validation - can be enhanced for specific countries
            if len(zip_code) < 3:
                raise ValidationError("ZIP code must be at least 3 characters long.")
        return zip_code


class BookSearchForm(forms.Form):
    """
    Form for searching books by title or author.

    Provides search functionality on the book listing page.
    """

    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title or author...',
            'autocomplete': 'off'
        }),
        help_text='Enter book title or author name'
    )

    category = forms.ChoiceField(
        choices=[
            ('all', 'All Categories'),
            ('fiction', 'Fiction'),
            ('non-fiction', 'Non-Fiction'),
            ('science', 'Science'),
            ('technology', 'Technology'),
            ('history', 'History'),
            ('biography', 'Biography'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    sort_by = forms.ChoiceField(
        choices=[
            ('title', 'Title A-Z'),
            ('-title', 'Title Z-A'),
            ('price', 'Price Low to High'),
            ('-price', 'Price High to Low'),
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
        ],
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.

    Allows users to update their personal and shipping information.
    """

    # Include User model fields
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )

    class Meta:
        model = UserProfile
        fields = [
            'phone_number',
            'date_of_birth',
            'default_shipping_address',
            'default_shipping_city',
            'default_shipping_state',
            'default_shipping_zip'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'default_shipping_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Default Shipping Address'
            }),
            'default_shipping_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'default_shipping_state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'default_shipping_zip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ZIP/Postal Code'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Pre-fill User model fields
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        """Save both User and UserProfile data"""
        profile = super().save(commit=False)
        user = profile.user

        # Update User model fields
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')

        if commit:
            user.save()
            profile.save()

        return profile


class ContactForm(forms.Form):
    """
    Contact form for customer support.

    Allows users to send messages to the bookstore administration.
    """

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your message...'
        })
    )

    def send_email(self):
        """Send contact form email (placeholder for future implementation)"""
        # TODO: Implement email sending functionality
        pass
