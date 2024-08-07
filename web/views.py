from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserLoginForm, InmuebleForm, CustomUserCreationForm, UserProfileForm, FiltroInmuebleForm,SolicitudArriendoForm, ActualizarSolicitudForm
from .models import Inmueble,UserData,Comuna,SolicitudArriendo

def index(request):
    # Obtener todos los inmuebles disponibles
    inmuebles = Inmueble.objects.all()
    if request.method == 'GET':
        form = FiltroInmuebleForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['region']:
                inmuebles = inmuebles.filter(comuna__region=form.cleaned_data['region'])
            if form.cleaned_data['comuna']:
                inmuebles = inmuebles.filter(comuna=form.cleaned_data['comuna'])
            if form.cleaned_data['tipo_inmueble']:
                inmuebles = inmuebles.filter(tipo_inmueble=form.cleaned_data['tipo_inmueble'])
    else:
        form = FiltroInmuebleForm()
    return render(request, 'pagina/index.html', {'form': form, 'inmuebles': inmuebles})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Autenticar y obtener las credenciales del usuario
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Iniciar sesión con el usuario autenticado
                login(request, user)
                # Redirigir a la página de inicio
                messages.success(request, f'Bienvenido {user.username}')
                return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'log/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo usuario
            user = form.save()
            # Crear una instancia de UserData para el nuevo usuario
            user_data = UserData(
                user=user,
                nombre=form.cleaned_data.get('nombre'),
                apellido=form.cleaned_data.get('apellido'),
                rut=form.cleaned_data.get('rut'),
                direccion=form.cleaned_data.get('direccion'),
                telefono=form.cleaned_data.get('telefono'),
                email=form.cleaned_data.get('email'),
                tipo_usuario=form.cleaned_data.get('tipo_usuario')
            )
            # Guardar los datos del usuario en la base de datos
            user_data.save()
            # Iniciar sesión con el nuevo usuario
            login(request, user)
            # Redirigir a la página de inicio
            return redirect('index')
    else:
        form = CustomUserCreationForm()
        # Renderizar la plantilla de registro con el formulario correspondiente
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_profile(request):
    # Obtener los datos del usuario actual
    user_data = UserData.objects.get(user=request.user)
    # Renderizar la plantilla con los datos del perfil del usuario
    return render(request, 'account/profile.html', {'user_data': user_data})

@login_required
def edit_profile(request):
    # Obtener los datos del usuario actual
    user_data = UserData.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_data)
        if form.is_valid():
            # Guardar los cambios de los datos del usuario en la base de datos
            form.save()
            # Redirigir al perfil del usuario
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_data)
    return render(request, 'account/edit_profile.html', {'form': form})

@login_required
def user_logout(request):
    # Cerrar sesión del usuario
    if request.method == 'POST':
        logout(request)
        # Redirigir a la página de inicio
        return redirect('index')
    return render(request, 'log/logout.html')

@login_required
def agregar_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el nuevo inmueble pero sin comprometerlo aún en la base de datos
            inmueble = form.save(commit=False)
            # Asignar el usuario actual como arrendador del inmueble
            inmueble.arrendador = request.user
            # Guardar el inmueble en la base de datos
            inmueble.save()
            # Redirigir a la página de inicio
            return redirect('index')
    else:
        form = InmuebleForm()
    return render(request, 'pagina/agregar_inmueble.html', {'form': form})

@login_required
def editar_inmueble(request, id):
    # Obtener el inmueble correspondiente o devolver un error 404 si no existe
    inmueble = get_object_or_404(Inmueble, id=id, arrendador=request.user)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES, instance=inmueble)
        if form.is_valid():
            # Guardar los cambios del inmueble en la base de datos
            form.save()
            return redirect('index')
    else:
        form = InmuebleForm(instance=inmueble)
    return render(request, 'pagina/editar_inmueble.html', {'form': form})


def detalle_inmueble(request, id):
    # Obtener el inmueble correspondiente o devolver un error 404 si no existe
    inmueble = get_object_or_404(Inmueble, id=id)
    return render(request, 'pagina/detalle_inmueble.html', {'inmueble': inmueble})

@login_required
def eliminar_inmueble(request, id):
    # Obtener el inmueble correspondiente o devolver un error 404 si no existe
    inmueble = get_object_or_404(Inmueble, id=id, arrendador=request.user)
    if request.method == 'POST':
        # Eliminar el inmueble de la base de datos
        inmueble.delete()
        # Redirigir a la página de inicio
        return redirect('index')
    # Renderizar la plantilla para confirmar la eliminación del inmueble
    return render(request, 'pagina/eliminar_inmueble.html', {'inmueble': inmueble})


def comunas_por_region(request, region_id):
    comunas = Comuna.objects.filter(region_id=region_id).order_by('nombre')
    comunas_dict = {comuna.id: comuna.nombre for comuna in comunas}
    return JsonResponse(comunas_dict)

@login_required
def postular_arriendo(request, inmueble_id):
    # Obtener el inmueble correspondiente o devolver un error 404 si no existe
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    if request.method == 'POST':
        form = SolicitudArriendoForm(request.POST)
        if form.is_valid():
            # Guardar la nueva solicitud de arriendo pero sin comprometerla aún en la base de datos
            solicitud = form.save(commit=False)
            # Asignar el usuario actual como arrendatario de la solicitud
            solicitud.arrendatario = request.user
            # Asignar el inmueble correspondiente a la solicitud
            solicitud.inmueble = inmueble
            # Guardar la solicitud en la base de datos
            solicitud.save()
            return redirect('index')
    else:
        form = SolicitudArriendoForm()
        # Renderizar la plantilla para postular a un arriendo con el formulario correspondiente
    return render(request, 'pagina/postular_arriendo.html', {'form': form, 'inmueble': inmueble})

@login_required
def listar_solicitudes(request):
    # Obtener los inmuebles del arrendador actual
    inmuebles = Inmueble.objects.filter(arrendador=request.user)
    # Obtener las solicitudes de arriendo para esos inmuebles, ordenadas por fecha de solicitud
    solicitudes = SolicitudArriendo.objects.filter(inmueble__in=inmuebles).order_by('-fecha_solicitud')
    # Renderizar la plantilla para listar las solicitudes con la lista de solicitudes
    return render(request, 'pagina/listar_solicitudes.html', {'solicitudes': solicitudes})

@login_required
def actualizar_solicitud(request, solicitud_id):
    # Obtener la solicitud correspondiente o devolver un error 404 si no existe
    solicitud = get_object_or_404(SolicitudArriendo, id=solicitud_id, inmueble__arrendador=request.user)
    if request.method == 'POST':
        form = ActualizarSolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            # Guardar los cambios de la solicitud en la base de datos
            form.save()
            # Redirigir a la página de listar solicitudes
            return redirect('listar_solicitudes')
    else:
        form = ActualizarSolicitudForm(instance=solicitud)
    return render(request, 'pagina/actualizar_solicitud.html', {'form': form, 'solicitud': solicitud})

@login_required
def listar_solicitudes_arrendatario(request):
    # Obtener las solicitudes del arrendatario actual, ordenadas por fecha de solicitud
    solicitudes = SolicitudArriendo.objects.filter(arrendatario=request.user).order_by('-fecha_solicitud')
    # Renderizar la plantilla para listar las solicitudes del arrendatario con la lista de solicitudes
    return render(request, 'pagina/listar_solicitudes_arrendatario.html', {'solicitudes': solicitudes})