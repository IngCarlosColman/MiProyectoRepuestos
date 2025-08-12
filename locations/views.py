# locations/views.py

from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from .models import Branch, Professional

def home(request):
    # 1. Obtener el término de búsqueda del formulario
    query = request.GET.get('q')

    # 2. Inicializar los QuerySets para sucursales y profesionales
    branches = Branch.objects.all()
    professionals = Professional.objects.all()

    # 3. Si hay un término de búsqueda, filtramos los resultados
    if query:
        branches = branches.filter(name__icontains=query)
        professionals = professionals.filter(workshop_name__icontains=query)
        
    # 4. Convertimos los datos de los modelos a un formato JSON geoespacial
    branches_geojson = serialize('geojson', branches, geometry_field='location', fields=('name', 'address'))
    professionals_geojson = serialize('geojson', professionals, geometry_field='location', fields=('workshop_name', 'address'))

    # 5. Pasamos los datos al contexto de la plantilla
    context = {
        'branches': branches,
        'professionals': professionals,
        'query': query,
        'branches_geojson': branches_geojson,
        'professionals_geojson': professionals_geojson,
    }
    
    return render(request, 'tailadmin/home.html', context)