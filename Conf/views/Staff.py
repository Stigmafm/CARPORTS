
import sys, traceback, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from Conf.models import Staff
from Login.models import auth_user_extend

class listStaff(ListView): 
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'Conf.view_staff':
                    pFlag = True
            if pFlag or request.user.is_staff:
                cntxStaff = Staff.objects.all()     
                cntx = {
                    'user': request.user,
                    'cntxStaff': cntxStaff,
                }
                return render(request, "ConfStaff/listStaff.html", cntx)
            else:
                return render(request, '403.html')

class addStaff(CreateView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_staff':
                    pFlag = True
            if pFlag or request.user.is_staff:
                cntx = {
                    'user': request.user,
                    'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                }
               
                return render(request, 'ConfStaff/addStaff.html', cntx)
            else:
                return render(request, '403.html')
        
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_staff':
                    pFlag = True
            if pFlag or request.user.is_staff:               

                if request.POST.get('Active')=='on': 
                    Active = True
                else:
                    Active = False

                StaffReg = Staff(
                    Name = request.POST.get('Name'),
                    Description = request.POST.get('Description'),
                    Block = Active
                )

                try:
                    StaffReg.save()                    

                    return redirect("/conf/staff/#23")
                except:
                    traceback.print_exc()  
                    return redirect("/conf/staff/#21")
            else:
                return render(request, '403.html')

class modStaff(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_staff':
                    pFlag = True
            if pFlag or request.user.is_staff:
                               
                cntxStaff = Staff.objects.get(id=self.kwargs['idStaff'])

                cntx = {
                        'user': request.user,
                        'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                        'Name':cntxStaff.Name,
                        'Description':cntxStaff.Description,
                        'Block':cntxStaff.Block
                    }
                return render(request, 'ConfStaff/modStaff.html', cntx)
            else:
                return render(request, '403.html')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_staff':
                    pFlag = True
            if pFlag or request.user.is_staff:
            
                cntxStaff = Staff.objects.get(id=self.kwargs['idStaff'])

                cntxStaff.Name = request.POST.get('Name')
                cntxStaff.Description = request.POST.get('Description')

                if request.POST.get('Active')=='on': 
                    cntxStaff.Block = True
                else:
                    cntxStaff.Block = False

                try:
                    cntxStaff.save()                 
                    return redirect('/conf/staff/mod/'+str(cntxStaff.id)+'/#23')
                except:
                    return redirect('/conf/staff/mod/'+str(cntxStaff.id)+'/#21')

            else:
                return render(request, '403.html')

class delStaff(DeleteView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.del_staff':
                    pFlag = True
            if pFlag or request.user.is_staff:
                if request.is_ajax():
                    try:
                        Staff.objects.get(id=request.GET.get('staffID')).delete()                        
                        request.session["saveStatus"] = 1
                    except:
                        # traceback.print_exc()  
                        request.session["saveStatus"] = 0

                    cntxAjax = {
                        'status': request.session["saveStatus"]
                    }
                    return JsonResponse(cntxAjax)

                if (request.session["saveStatus"] == 1):
                    return redirect('/conf/staff/#22')
                else:
                    return redirect('/conf/staff/#21')

            else:
                return render(request, '403.html')
