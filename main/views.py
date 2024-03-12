from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.models import User


@login_required(login_url='/login/')
def home(request):
    return render(request, 'core/home.html')

def login(request):
    mensaje = ''

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
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
