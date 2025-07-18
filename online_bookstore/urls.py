"""
URL configuration for online_bookstore project.

This is the main URL configuration file that routes requests to
the appropriate app-specific URL configurations.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),

    # Include store app URLs
    path('', include('store.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin interface
admin.site.site_header = "Online Bookstore Admin"
admin.site.site_title = "Bookstore Admin Portal"
admin.site.index_title = "Welcome to Bookstore Administration"