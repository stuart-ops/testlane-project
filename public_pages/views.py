from django.shortcuts import render


def landing_page(request):
    """Public landing page - no authentication required."""
    return render(request, 'public_pages/landing.html')


def about_us(request):
    """About us page - no authentication required."""
    return render(request, 'public_pages/about.html')
