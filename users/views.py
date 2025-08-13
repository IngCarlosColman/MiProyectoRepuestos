# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# from .models import Notification  # Descomenta esta línea si ya tienes un modelo de notificaciones

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def account_settings(request):
    return render(request, 'users/account_settings.html')

@login_required
def support(request):
    return render(request, 'users/support.html')

@login_required
def all_notifications(request):
    # Lógica para obtener todas las notificaciones
    # notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {'notifications': []} # Usa una lista vacía de forma temporal
    return render(request, 'users/all_notifications.html', context)

def logout_view(request):
    logout(request)
    # Redirige a la página de inicio de sesión. Cambia 'login' si tu URL se llama diferente.
    return redirect('login')