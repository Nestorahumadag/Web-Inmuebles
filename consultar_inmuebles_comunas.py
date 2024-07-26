import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inmuebles.settings")
django.setup()

from web.models import Inmueble

def consultar_inmuebles_por_comunas():
    inmuebles = Inmueble.objects.select_related('comuna').all()
    resultados = {}
    for inmueble in inmuebles:
        comuna = inmueble.comuna.nombre
        if comuna not in resultados:
            resultados[comuna] = []
        resultados[comuna].append(inmueble)

    with open('inmuebles_por_comunas.txt', 'w', encoding='utf-8') as f:
        for comuna, inmuebles in resultados.items():
            f.write(f"Comuna: {comuna}\n")
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
    consultar_inmuebles_por_comunas()