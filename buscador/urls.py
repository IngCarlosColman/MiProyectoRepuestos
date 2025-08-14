from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    # Ruta para la aplicación de React
    # Esta es la ruta principal que servirá el index.html
    path('', views.index, name='index'),

    # Rutas para la API REST
    path('api/repuestos/', views.RepuestoGlobalList.as_view(), name='repuesto-list'),
]

urlpatterns += router.urls
