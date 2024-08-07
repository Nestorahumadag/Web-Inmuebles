from django.db import models
from django.contrib.auth.models import User

# models.py de la aplicación "web"

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_data')# Relación uno a uno con el usuario
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=50, choices=[('arrendador', 'Arrendador'), ('arrendatario', 'Arrendatario')])# Campo de texto para el tipo de usuario

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)# Relación con la región, se elimina en cascada

    def __str__(self):
        return self.nombre

class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Inmueble(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    m2_construidos = models.FloatField()
    m2_totales = models.FloatField()
    cantidad_estacionamientos = models.IntegerField()
    cantidad_habitaciones = models.IntegerField()
    cantidad_banos = models.IntegerField()
    direccion = models.CharField(max_length=255)
    precio_mensual_arriendo = models.DecimalField(max_digits=10, decimal_places=2)
    comuna = models.ForeignKey('Comuna', on_delete=models.CASCADE)# Relación con la comuna, se elimina en cascada
    arrendador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inmuebles')# Relación con el usuario arrendador
    disponible = models.BooleanField(default=True)# Campo booleano para indicar si el inmueble está disponible
    imagen = models.ImageField(upload_to='inmuebles/', null=True, blank=True)# Campo de imagen para subir fotos del inmueble
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class SolicitudArriendo(models.Model):
    arrendatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes')# Relación con el usuario arrendatario
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='solicitudes')# Relación con el inmueble
    fecha_solicitud = models.DateTimeField(auto_now_add=True)# Fecha y hora de la solicitud, se establece automáticamente
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')], default='pendiente')

    def __str__(self):
        return f"Solicitud de {self.arrendatario.username} para {self.inmueble.nombre}"
    

