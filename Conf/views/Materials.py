
import sys, traceback, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from Conf.models import Materials

class listMaterials(ListView): 
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'Conf.view_materials':
                    pFlag = True
            if pFlag or request.user.is_staff:
                cntxMaterials = Materials.objects.all()     
                cntx = {
                    'user': request.user,
                    'cntxMaterials': cntxMaterials,
                }
                return render(request, "ConfMaterials/listMaterials.html", cntx)
            else:
                return render(request, '403.html')
        
class addMaterials(CreateView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_materials':
                    pFlag = True
            if pFlag or request.user.is_staff:
                cntx = {
                    'user': request.user,
                }
               
                return render(request, 'ConfMaterials/addMaterials.html', cntx)
            else:
                return render(request, '403.html')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_materials':
                    pFlag = True
            if pFlag or request.user.is_staff:               

                if request.POST.get('Active')=='on': 
                    Active = True
                else:
                    Active = False
                
                if request.POST.get('Dependent')=='on': 
                    Dependent = True
                    Size = request.POST.get('select_TypeSize')
                else:
                    Dependent = False
                    Size = None

                MaterialsReg = Materials(
                    Name = request.POST.get('Name'),
                    Description = request.POST.get('Description'),
                    Dependent = Dependent,
                    Sizes = Size,
                    Block = Active
                )

                try:
                    MaterialsReg.save()                    

                    return redirect("/conf/materials/#23")
                except:
                    traceback.print_exc()  
                    return redirect("/conf/materials/#21")
            else:
                return render(request, '403.html')

class modMaterials(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_materials':
                    pFlag = True
            if pFlag or request.user.is_staff:
                               
                cntxMaterial = Materials.objects.get(id=self.kwargs['idMaterial'])

                cntx = {
                        'user': request.user,
                        'Name':cntxMaterial.Name,
                        'Description':cntxMaterial.Description,
                        'Dependent': cntxMaterial.Dependent,
                        'Sizes': cntxMaterial.Sizes,
                        'Block':cntxMaterial.Block
                    }
                return render(request, 'ConfMaterials/modMaterials.html', cntx)
            else:
                return render(request, '403.html')
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_materials':
                    pFlag = True
            if pFlag or request.user.is_staff:
            
                cntxMaterial = Materials.objects.get(id=self.kwargs['idMaterial'])

                cntxMaterial.Name = request.POST.get('Name')
                cntxMaterial.Description = request.POST.get('Description')

                if request.POST.get('Active')=='on': 
                    cntxMaterial.Block = True
                else:
                    cntxMaterial.Block = False

                if request.POST.get('Dependent')=='on': 
                    cntxMaterial.Dependent = True
                    cntxMaterial.Sizes = request.POST.get('select_TypeSize')
                else:
                    cntxMaterial.Dependent = False
                    cntxMaterial.Sizes = None

                try:
                    cntxMaterial.save()                 
                    return redirect('/conf/materials/mod/'+str(cntxMaterial.id)+'/#23')
                except:
                    return redirect('/conf/materials/mod/'+str(cntxMaterial.id)+'/#21')

            else:
                return render(request, '403.html')

class delMaterials(DeleteView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.del_materials':
                    pFlag = True
            if pFlag or request.user.is_staff:
                if request.is_ajax():
                    try:
                        Materials.objects.get(id=request.GET.get('materialID')).delete()                        
                        request.session["saveStatus"] = 1
                    except:
                        # traceback.print_exc()  
                        request.session["saveStatus"] = 0

                    cntxAjax = {
                        'status': request.session["saveStatus"]
                    }
                    return JsonResponse(cntxAjax)

                if (request.session["saveStatus"] == 1):
                    return redirect('/conf/materials/#22')
                else:
                    return redirect('/conf/materials/#21')

            else:
                return render(request, '403.html')
