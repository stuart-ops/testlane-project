from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.landing_page, name='landing'),
    path('about/', views.about_us, name='about'),
]
