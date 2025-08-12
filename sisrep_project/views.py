# views.py
from django.shortcuts import render

def home(request):
    return render(request, 'tailadmin/index.html')

def profile(request):
    # Esta vista ya funciona porque profile.html existe
    return render(request, 'tailadmin/profile.html')

# Vista temporal para mensajes y configuraciones
def placeholder_view(request):
    # Puedes crear un archivo placeholder.html o usar index.html
    return render(request, 'tailadmin/index.html')