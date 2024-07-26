from django.db import models

# models.py de la aplicación "web"

class User(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    rut = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=255)
    telefono_personal = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=50, choices=[('arrendador', 'Arrendador'), ('arrendatario', 'Arrendatario')])

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='comunas')

    def __str__(self):
        return self.nombre

class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Inmueble(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    m2_construidos = models.DecimalField(max_digits=10, decimal_places=2)
    m2_totales = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_estacionamientos = models.IntegerField()
    cantidad_habitaciones = models.IntegerField()
    cantidad_banos = models.IntegerField()
    direccion = models.CharField(max_length=255)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, related_name='inmuebles')
    tipo_inmueble = models.CharField(max_length=20, choices=[('casa', 'Casa'), ('departamento', 'Departamento'), ('parcela', 'Parcela')])
    precio_mensual_arriendo = models.DecimalField(max_digits=10, decimal_places=2)
    arrendador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inmuebles', limit_choices_to={'tipo_usuario': 'arrendador'})

    def __str__(self):
        return self.nombre

class SolicitudArriendo(models.Model):
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='solicitudes')
    arrendatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes', limit_choices_to={'tipo_usuario': 'arrendatario'})
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado_solicitud = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')])

    def __str__(self):
        return f"solicitud de {self.arrendatario.nombres} para {self.inmueble.nombre}"
    

