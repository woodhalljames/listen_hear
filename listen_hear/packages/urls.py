"""URLs for packages app"""
from django.urls import path
from . import views

app_name = 'packages'

urlpatterns = [
    path('', views.PackageListView.as_view(), name='list'),
    path('<int:pk>/', views.PackageDetailView.as_view(), name='detail'),
    path('category/<int:category_id>/', views.CategoryPackageListView.as_view(), name='category_list'),
]
