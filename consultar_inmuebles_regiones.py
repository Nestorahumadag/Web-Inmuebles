# consultar_inmuebles_regiones.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inmuebles.settings")
django.setup()

from web.models import Inmueble

def consultar_inmuebles_por_regiones():
    inmuebles = Inmueble.objects.select_related('comuna__region').all()
    resultados = {}
    for inmueble in inmuebles:
        region = inmueble.comuna.region.nombre
        if region not in resultados:
            resultados[region] = []
        resultados[region].append(inmueble)

    with open('inmuebles_por_regiones.txt', 'w', encoding='utf-8') as f:
        for region, inmuebles in resultados.items():
            f.write(f"Región: {region}\n")
            for inmueble in inmuebles:
                f.write(f"  - Nombre: {inmueble.nombre}\n")
                f.write(f"    Descripción: {inmueble.descripcion}\n")
                f.write(f"    M2 Construidos: {inmueble.m2_construidos}\n")
                f.write(f"    M2 Totales: {inmueble.m2_totales}\n")
                f.write(f"    Estacionamientos: {inmueble.cantidad_estacionamientos}\n")
                f.write(f"    Habitaciones: {inmueble.cantidad_habitaciones}\n")
                f.write(f"    Baños: {inmueble.cantidad_banos}\n")
                f.write(f"    Dirección: {inmueble.direccion}\n")
                f.write(f"    Precio Mensual de Arriendo: {inmueble.precio_mensual_arriendo}\n")
                f.write("\n")

if __name__ == "__main__":
    consultar_inmuebles_por_regiones()
