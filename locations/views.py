# locations/views.py

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.serializers import serialize
from django.utils import timezone
import json

from .models import Branch, Professional, Store, Product


def get_business_status(business):
    """
    Determina si un negocio está abierto o cerrado basándose en el día y la hora actual.
    """
    now = timezone.localtime(timezone.now())
    today = now.strftime('%a').upper()[:3]
    current_time = now.time()
    
    is_open = False
    status_text = 'Cerrado'

    if business.days_of_week and today in business.days_of_week:
        if business.opening_time and business.closing_time:
            if business.opening_time <= current_time <= business.closing_time:
                is_open = True
                status_text = 'Abierto ahora'
            
    return {'is_open': is_open, 'status_text': status_text}


def home(request):
    all_stores = Store.objects.all()
    all_branches = Branch.objects.all()
    all_professionals = Professional.objects.all()

    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Agrega tiendas al GeoJSON
    for loc in all_stores:
        feature = {
            "type": "Feature",
            "geometry": json.loads(loc.location.geojson),
            "properties": {
                "type": "store",
                "name": loc.name,
                "url": f"/stores/{loc.id}/",
                "is_open": get_business_status(loc)['is_open'],
                "address": loc.address
            }
        }
        geojson_data["features"].append(feature)

    # Agrega sucursales al GeoJSON
    for loc in all_branches:
        feature = {
            "type": "Feature",
            "geometry": json.loads(loc.location.geojson),
            "properties": {
                "type": "branch",
                "name": loc.name,
                "url": f"/branches/{loc.id}/",
                "is_open": get_business_status(loc)['is_open'],
                "address": loc.address
            }
        }
        geojson_data["features"].append(feature)
        
    # Agrega profesionales al GeoJSON
    for loc in all_professionals:
        feature = {
            "type": "Feature",
            "geometry": json.loads(loc.location.geojson),
            "properties": {
                "type": "professional",
                "name": loc.workshop_name,
                "url": f"/professionals/{loc.id}/",
                "is_open": get_business_status(loc)['is_open'],
                "address": loc.address
            }
        }
        geojson_data["features"].append(feature)
    
    context = {
        'stores': all_stores,
        'branches': all_branches,
        'professionals': all_professionals,
        'home_geojson': json.dumps(geojson_data),
        'service_types': Professional.SERVICE_TYPES,
    }
    
    # RENDERIZA LA PLANTILLA CORREGIDA
    return render(request, 'locations/home.html', context)


def search_results(request):
    query = request.GET.get('q', '')
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    
    if query:
        # Lógica de búsqueda para tiendas
        all_stores = Store.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query)
        ).distinct()
        
        # Lógica de búsqueda para sucursales
        all_branches = Branch.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query)
        ).distinct()

        # Lógica de búsqueda para profesionales
        all_professionals = Professional.objects.filter(
            Q(workshop_name__icontains=query) |
            Q(address__icontains=query)
        ).distinct()

        # Lógica para crear el GeoJSON de los resultados encontrados
        for store in all_stores:
            feature = {
                "type": "Feature",
                "geometry": json.loads(store.location.geojson),
                "properties": {
                    "type": "store",
                    "name": store.name,
                    "url": f"/stores/{store.id}/",
                    "address": store.address
                }
            }
            geojson_data["features"].append(feature)
        
        for branch in all_branches:
            feature = {
                "type": "Feature",
                "geometry": json.loads(branch.location.geojson),
                "properties": {
                    "type": "branch",
                    "name": branch.name,
                    "url": f"/branches/{branch.id}/",
                    "address": branch.address
                }
            }
            geojson_data["features"].append(feature)
            
        for professional in all_professionals:
            feature = {
                "type": "Feature",
                "geometry": json.loads(professional.location.geojson),
                "properties": {
                    "type": "professional",
                    "name": professional.workshop_name,
                    "url": f"/professionals/{professional.id}/",
                    "address": professional.address
                }
            }
            geojson_data["features"].append(feature)
    else:
        all_stores = Store.objects.none()
        all_branches = Branch.objects.none()
        all_professionals = Professional.objects.none()
        
    context = {
        'query': query,
        'stores': all_stores,
        'branches': all_branches,
        'professionals': all_professionals,
        'search_geojson': json.dumps(geojson_data),
    }

    return render(request, 'locations/search_results.html', context)


def branch_detail(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": json.loads(branch.location.geojson),
                "properties": {
                    "name": branch.name,
                }
            }
        ]
    }
    
    context = {
        'branch': branch,
        'branch_geojson': json.dumps(geojson_data),
    }
    # RENDERIZA LA PLANTILLA CORREGIDA
    return render(request, 'locations/branch_detail.html', context)


def professional_detail(request, pk):
    professional = get_object_or_404(Professional, pk=pk)

    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": json.loads(professional.location.geojson),
                "properties": {
                    "name": professional.workshop_name,
                }
            }
        ]
    }

    context = {
        'professional': professional,
        'professional_geojson': json.dumps(geojson_data),
    }
    # RENDERIZA LA PLANTILLA CORREGIDA
    return render(request, 'locations/professional_detail.html', context)


def store_detail(request, pk):
    store = get_object_or_404(Store, pk=pk)
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": json.loads(store.location.geojson),
                "properties": {
                    "name": store.name,
                }
            }
        ]
    }
    
    context = {
        'store': store,
        'store_geojson': json.dumps(geojson_data),
    }
    # RENDERIZA LA PLANTILLA CORREGIDA
    return render(request, 'locations/store_detail.html', context)