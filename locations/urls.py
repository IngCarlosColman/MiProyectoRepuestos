# locations/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Cambia la vista para que renderice la nueva plantilla
    path('', views.home, name='home'),
]