from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('agregar_inmueble/', views.agregar_inmueble, name='agregar_inmueble'),
    path('editar_inmueble/<int:id>/', views.editar_inmueble, name='editar_inmueble'),
    path('eliminar_inmueble/<int:id>/', views.eliminar_inmueble, name='eliminar_inmueble'),
    path('comunas/<int:region_id>/', views.comunas_por_region, name='comunas_por_region'),
    path('detalle_inmueble/<int:id>/', views.detalle_inmueble, name='detalle_inmueble'),
    path('postular_arriendo/<int:inmueble_id>/', views.postular_arriendo, name='postular_arriendo'),
    path('solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),
    path('solicitud/<int:solicitud_id>/', views.actualizar_solicitud, name='actualizar_solicitud'),
    path('mis_solicitudes/', views.listar_solicitudes_arrendatario, name='listar_solicitudes_arrendatario'),
    path('solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),
    path('solicitud/<int:solicitud_id>/', views.actualizar_solicitud, name='actualizar_solicitud'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)