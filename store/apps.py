"""
Django app configuration for the store application.

This module contains the application configuration for the store app,
including any startup tasks and signal connections.
"""

from django.apps import AppConfig


class StoreConfig(AppConfig):
    """
    Configuration for the store application.

    This class defines the configuration for the store app and handles
    any initialization tasks that need to be performed when the app starts.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    verbose_name = 'Online Bookstore'

    def ready(self):
        """
        This method is called when the application is ready.

        It's used to perform any initialization tasks such as
        connecting signal handlers or importing modules that
        define signal handlers.
        """
        # Import signal handlers (if any)
        try:
            from . import signals
        except ImportError:
            pass

        # Register any custom checks (if needed)
        # from . import checks
