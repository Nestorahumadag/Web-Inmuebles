# services.py en la aplicación "web"
from .models import Inmueble, User, SolicitudArriendo, Comuna

# Funciones para inmuebles
def crear_inmueble(datos_inmueble):
    inmueble = Inmueble.objects.create(**datos_inmueble)
    return inmueble

def listar_inmuebles():
    return Inmueble.objects.all()

def actualizar_inmueble(inmueble_id, nuevos_datos):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    for key, value in nuevos_datos.items():
        setattr(inmueble, key, value)
    inmueble.save()
    return inmueble

def borrar_inmueble(inmueble_id):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    inmueble.delete()
    return inmueble

# Funciones para usuarios
def crear_usuario(datos_usuario):
    usuario = User.objects.create(**datos_usuario)
    return usuario

def listar_usuarios():
    return User.objects.all()

def actualizar_usuario(usuario_id, nuevos_datos):
    usuario = User.objects.get(id=usuario_id)
    for key, value in nuevos_datos.items():
        setattr(usuario, key, value)
    usuario.save()
    return usuario

def borrar_usuario(usuario_id):
    usuario = User.objects.get(id=usuario_id)
    usuario.delete()
    return usuario

# Funciones para solicitudes de arriendo
def crear_solicitud_arriendo(datos_solicitud):
    solicitud = SolicitudArriendo.objects.create(**datos_solicitud)
    return solicitud

def listar_solicitudes():
    return SolicitudArriendo.objects.all()

def actualizar_solicitud(solicitud_id, nuevos_datos):
    solicitud = SolicitudArriendo.objects.get(id=solicitud_id)
    for key, value in nuevos_datos.items():
        setattr(solicitud, key, value)
    solicitud.save()
    return solicitud

def borrar_solicitud(solicitud_id):
    solicitud = SolicitudArriendo.objects.get(id=solicitud_id)
    solicitud.delete()
    return solicitud

# Funciones para comunas
def crear_comuna(nombre):
    comuna = Comuna.objects.create(nombre=nombre)
    return comuna

def listar_comunas():
    return Comuna.objects.all()

def borrar_comuna(comuna_id):
    comuna = Comuna.objects.get(id=comuna_id)
    comuna.delete()
    return comuna
