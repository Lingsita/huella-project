# -*- encoding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from Accounts.models import UserSession
import uuid
import constantes
# Create your views here.

def index (request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return admin_empresas(request)
        else:
            return render(request, 'empleado.html', {})
    else:
        if request.method =="POST":
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            print request.POST['username']
            if user is not None :
                # the password verified for the user
                if user.is_active:
                    login(request, user)
                    device_uuid = str(uuid.uuid4())
                    userSession=UserSession(user=user, ip = device_uuid, active=True)
                    userSession.save()
                    request.session['uu_id'] = device_uuid
                    if user.is_superuser:
                        return admin_empresas(request)
                    else:
                        return render(request, 'empleado.html', {})
                else:
                    return render(request, 'inicio_sesion.html', {'error_message': constantes.NO_AUTH_USER})
            else:
                # the authentication system was unable to verify the username and password
                return render(request, 'inicio_sesion.html', {'error_message': constantes.NO_AUTH_USER})
        return render(request, 'inicio_sesion.html', {})

def admin_empresas(request):
    return render(request, 'admin.html', {})



def logout_session(request):
    try:
        userSession=UserSession.objects.get(ip = request.session['uu_id'])
        userSession.active=False
        userSession.save()
    except UserSession.DoesNotExist:
        print "no exite el identificador de session"
    logout(request)
    return redirect('index')