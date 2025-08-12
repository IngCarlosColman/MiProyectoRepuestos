# locations/views.py

from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from .models import Branch, Professional

def home(request):
    query = request.GET.get('q')
    branches = Branch.objects.all()
    professionals = Professional.objects.all()

    if query:
        branches = branches.filter(name__icontains=query)
        professionals = professionals.filter(workshop_name__icontains=query)

    branches_geojson = serialize('geojson', branches, geometry_field='location', fields=('name', 'address'))
    professionals_geojson = serialize('geojson', professionals, geometry_field='location', fields=('workshop_name', 'address'))

    context = {
        'branches': branches,
        'professionals': professionals,
        'query': query,
        'branches_geojson': branches_geojson,
        'professionals_geojson': professionals_geojson,
    }

    # Change the template name here to reflect the new file
    return render(request, 'tailadmin/home.html', context)