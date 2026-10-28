from django.shortcuts import render, redirect


def landing_page(request):
    """Public landing page - showcases agentic AI simulation engine, video tour, and interactive playground."""
    return render(request, 'public_pages/landing.html')


def demo_page(request):
    """Interactive demo showcase page."""
    return render(request, 'public_pages/demo.html')


def about_us(request):
    """About us page - company mission, leadership, and contact."""
    return render(request, 'public_pages/about.html')
