__author__ = 'linglung'
from Accounts import constantes
from django.contrib.auth import  logout
from Accounts.models import UserSession
from django.shortcuts import render

from django.contrib.auth.models import User

class OnlyOneSession(object):
    def process_request(self, request):
        if request.user.is_anonymous():
            return None
        else:
            try:
                userSessions = UserSession.objects.filter(user=request.user, active=True).order_by('date_joined')
                actual_session=UserSession.objects.get(user=request.user, active=True, ip=request.session['uu_id'])
                for us in userSessions:
                    if us.date_joined > actual_session.date_joined:
                        actual_session.active=False
                        actual_session.save()
                        logout(request)
                        return render(request, 'one_session.html', {'error_message': constantes.ONLY_ONE_SESSION})
            except UserSession.DoesNotExist:
                logout(request)
                return render(request, 'inicio_sesion.html', {'error_message': constantes.ONLY_ONE_SESSION})
                # print("el usuario no es anonimo, es:{0}".format(request.user.username))
        return None