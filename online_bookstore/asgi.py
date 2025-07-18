"""
ASGI config for online_bookstore project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_bookstore.settings')

application = get_asgi_application()
