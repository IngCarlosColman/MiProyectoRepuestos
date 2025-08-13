# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('support/', views.support, name='support'),
    path('logout/', views.logout_view, name='logout'),
    path('notifications/', views.all_notifications, name='all_notifications'),
]