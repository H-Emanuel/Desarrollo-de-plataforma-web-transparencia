from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from crud.models import *
from django.db.models import Count, Value
from django.db.models.functions import Lower, Concat

import json

@login_required(login_url='/login/')
def home(request):
    user = request.user
    departamento_usuario = Departamento.objects.filter(id_usuario=user).first()
    data = {
        'departamento':departamento_usuario
    }
    
    return render(request, 'core/home.html',data)


@login_required(login_url='/login/')
def cuadro_de_mando(request):
    # Obtener el total por estado
    total_por_estado = list(Solicitud.objects.values('estado').annotate(total=Count('estado')))

    # Obtener el total por nombre o razón social, ignorando mayúsculas y minúsculas
    total_por_nombre = list(Solicitud.objects.annotate(
        nombre_completo_lower=Lower(
            Concat(
                'nombre_o_razon_social', Value(' '), 
                'primer_apellido', Value(' '), 
                'segundo_apellido'
            )
        )
    ).values('nombre_completo_lower').annotate(total=Count('nombre_completo_lower')))

    contexto = {
        'total_por_estado': json.dumps(total_por_estado),
        'total_por_nombre': json.dumps(total_por_nombre),
    }

    return render(request, 'core/Cuadro_De_mando.html', contexto)



def login(request):
    mensaje = ''

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            mensaje = 'Usuario o contraseña incorrectos'
    
    data = {
        'mensaje': mensaje
    }
    return render(request, 'core/login.html', data)

def logout(request):
    auth_logout(request)
    return redirect('core_login')

def change_password(request):

    mensaje = ''

    if request.method == 'POST':
        password = request.POST['password1']
        password2 = request.POST['password2']
        if password == password2:
            user = User.objects.get(id=request.user.id)
            user.set_password(password)
            user.save()
            return redirect('home')
        else:
            mensaje = 'Las contraseñas no coinciden'

    context = {
        'mensaje': mensaje
    }

    return render(request, 'core/change_password.html', context)
