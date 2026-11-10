"""
URL configuration for Testlane.ai Sovereign AI platform.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public_pages.urls')),
]