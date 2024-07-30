from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Inmueble, UserData, Comuna, Region,SolicitudArriendo


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    rut = forms.CharField(max_length=10, required=True)
    direccion = forms.CharField(max_length=255, required=True)
    telefono = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    tipo_usuario = forms.ChoiceField(choices=[('arrendador', 'Arrendador'), ('arrendatario', 'Arrendatario')], required=True)# Campo de selección requerido para el tipo de usuario

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nombre', 'apellido', 'rut', 'direccion', 'telefono', 'email', 'tipo_usuario')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['nombre', 'apellido', 'direccion', 'telefono', 'tipo_usuario']

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'cantidad_estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'direccion', 'precio_mensual_arriendo', 'comuna', 'imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class FiltroInmuebleForm(forms.Form):
    # Campo de selección de región con datos del modelo Region, no es obligatorio
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Región", widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    # Campo de selección de comuna con datos del modelo Comuna, no es obligatorio y comienza vacío
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), required=False, label="Comuna", widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))

    def __init__(self, *args, **kwargs):
        # Llamada al constructor de la clase padre
        super().__init__(*args, **kwargs)#Constructor del formulario. Se llama al crear una instancia del formulario.
        # Verificar si hay datos de 'region' en la solicitud
        if 'region' in self.data:
            try:
                # Intentar convertir el ID de la región a un entero
                region_id = int(self.data.get('region'))
                # Actualizar el queryset del campo 'comuna' para filtrar las comunas por la región seleccionada
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                # Entrada no válida del cliente; ignorar y retroceder a un conjunto de consultas vacío
                pass
        else:
            # Si no hay datos de 'region', establecer el queryset de 'comuna' a vacío
            self.fields['comuna'].queryset = Comuna.objects.none()

class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        # El formulario está basado en el modelo SolicitudArriendo
        model = SolicitudArriendo
        # No hay campos específicos para el formulario, se utilizarán los campos predeterminados del modelo
        fields = []

class ActualizarSolicitudForm(forms.ModelForm):
    estado = forms.ChoiceField(choices=[('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')], required=True, label="Estado de la solicitud")

    class Meta:
        model = SolicitudArriendo
        fields = ['estado']# Campo del formulario