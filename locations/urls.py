# locations/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('branches/<int:pk>/', views.branch_detail, name='branch_detail'),
    path('professionals/<int:pk>/', views.professional_detail, name='professional_detail'),
    # NUEVA URL para el detalle de la tienda
    path('stores/<int:pk>/', views.store_detail, name='store_detail'),
]