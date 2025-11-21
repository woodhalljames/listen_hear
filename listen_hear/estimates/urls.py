"""URLs for estimates app"""
from django.urls import path
from . import views

app_name = 'estimates'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('thank-you/<str:estimate_number>/', views.thank_you, name='thank_you'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<str:estimate_number>/', views.estimate_detail, name='detail'),
]
