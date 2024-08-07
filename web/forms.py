from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Inmueble, UserData, Comuna, Region,SolicitudArriendo,TipoInmueble


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
        fields = [
            'nombre', 
            'descripcion', 
            'direccion', 
            'precio_mensual_arriendo', 
            'imagen', 
            'tipo_inmueble', 
            'comuna', 
            'cantidad_habitaciones', 
            'cantidad_banos', 
            'cantidad_estacionamientos', 
            'm2_construidos', 
            'm2_totales'
        ]
        labels = {
            'tipo_inmueble': 'Tipo de Inmueble',
            'cantidad_habitaciones': 'Habitaciones',
            'cantidad_banos': 'Baños',
            'cantidad_estacionamientos': 'Estacionamientos',
            'm2_construidos': 'Metros construidos',
            'm2_totales': 'Metros totales',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control w-50'}),
            'tipo_inmueble': forms.Select(attrs={'class': 'form-control w-50'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'precio_mensual_arriendo': forms.NumberInput(attrs={'class': 'form-control w-50'}),
            'cantidad_habitaciones': forms.NumberInput(attrs={'class': 'form-control w-50'}),
            'cantidad_banos': forms.NumberInput(attrs={'class': 'form-control w-50'}),
            'cantidad_estacionamientos': forms.NumberInput(attrs={'class': 'form-control w-50'}),
            'm2_construidos': forms.NumberInput(attrs={'class': 'form-control w-50'}),
            'm2_totales': forms.NumberInput(attrs={'class': 'form-control w-50'}),
            'comuna': forms.Select(attrs={'class': 'form-control w-50'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control w-50'}),
        }

class FiltroInmuebleForm(forms.Form):
    # Campo de selección de región con datos del modelo Region, no es obligatorio
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Región", widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'id_region'}),empty_label="")
    # Campo de selección de comuna con datos del modelo Comuna, no es obligatorio y comienza vacío
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), required=False, label="Comuna", widget=forms.Select(attrs={'class': 'form-control form-control-sm custom-select-width', 'id': 'id_comuna'}),empty_label="")
    # Campo de selección de tipo de inmueble con datos del modelo TipoInmueble, no es obligatorio y comienza vacío
    tipo_inmueble = forms.ModelChoiceField(queryset=TipoInmueble.objects.all(), required=False, label="Tipo de Inmueble",
                                           widget=forms.Select(attrs={'class': 'form-control form-control-sm custom-select-width'}),empty_label="")
    
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