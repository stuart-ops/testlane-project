from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('welcome/', views.landing_page, name='welcome'),
    path('demo/', views.demo_page, name='demo'),
    path('about/', views.about_us, name='about'),
]
