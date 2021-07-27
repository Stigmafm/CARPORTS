# coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView
from Login.models import auth_user_extend

# from Root.Session.models import auth_user_extend

# from ERP.Conf.ERPModeling.models import sSiteAuthUserExtend

class Index(FormView):
    # template_name = 'Index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            cntx = {
                # 'system':request.session["system"],
                # 'systemMin':request.session["systemMin"],
                'user': request.user,
                'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
            }
            # return render(request, 'Index.html', cntx)
            home = auth_user_extend.objects.get(AuthUserID=request.user.id).UrlHome
            if (home == '/'):
                return render(request, 'Index.html', cntx)
            else:
                return redirect(home)

# def error400(request):
#     return render(request, '400.html', status=404)

# def error403(request):
#     return render(request, '403.html', status=404)

# def error404(request):
#     return render(request, '404.html', status=404)

# def error500(request):
#     return render(request, '500.html', status=404)