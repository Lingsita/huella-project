__author__ = 'linglung'
from Accounts import constantes
from django.contrib.auth import  logout
from Accounts.models import UserSession
from django.shortcuts import render

from django.contrib.auth.models import User


class OnlyOneSession(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass
        # if request.user.is_anonymous():
        #     print "is an anonymous user"
        #
        #     return view_func(request, *view_args, **view_kwargs)
        # else:
        #     try:
        #         userSessions = UserSession.objects.filter(user=request.user, active=True).order_by('date_joined')
        #         # if 'uu_id' in request.session:
        #         actual_session=UserSession.objects.get(user=request.user, active=True, ip=request.session['uu_id'])
        #         for us in userSessions:
        #             if us.date_joined > actual_session.date_joined:
        #                 actual_session.active=False
        #                 actual_session.save()
        #                 logout(request)
        #                 return render(request, 'one_session.html', {'error_message': constantes.ONLY_ONE_SESSION})
        #         # else:
        #         #     print("there's no season")
        #
        #     except UserSession.DoesNotExist:
        #         logout(request)
        #         return render(request, 'inicio_sesion.html', {'error_message': constantes.ONLY_ONE_SESSION})
        #         # print("el usuario no es anonimo, es:{0}".format(request.user.username))
        #
        #     return view_func(request, *view_args, **view_kwargs)