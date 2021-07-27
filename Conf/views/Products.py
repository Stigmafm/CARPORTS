import sys, traceback, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from Conf.models import Products, Materials, ProductsAddMaterials
from Login.models import auth_user_extend

class listProducts(ListView): 
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'Conf.view_products':
                    pFlag = True
            if pFlag or request.user.is_staff:
                cntxProducts = Products.objects.all()     
                cntx = {
                    'user': request.user,
                    'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                    'cntxProducts': cntxProducts
                }
                return render(request, "ConfProducts/listProducts.html", cntx)
            else:
                return render(request, '403.html')

class addProducts(CreateView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_products':
                    pFlag = True
            if pFlag or request.user.is_staff:  
                cntxMaterials = Materials.objects.filter(Block = True)
                cntx = {
                    'user': request.user,
                    'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                    'cntxMaterials': cntxMaterials,
                }
               
                return render(request, 'ConfProducts/addProducts.html', cntx)
            else:
                return render(request, '403.html')
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_products':
                    pFlag = True
            if pFlag or request.user.is_staff:               

                if request.POST.get('Active')=='on': 
                    Active = True
                else:
                    Active = False

                ProductsReg = Products(
                    Name = request.POST.get('Name'),
                    Description = request.POST.get('Description'),
                    Block = Active
                )

                try:
                    ProductsReg.save() 

                    if(request.POST.get('input_dataMaterials') != ''):
                        dp = []
                        tmp = []
                        y = 0 
                        dataMaterials = request.POST.get("input_dataMaterials").split(",")
                        print(dataMaterials)
                        for x in range(0, len(dataMaterials)):
                            if (y<2):                         
                                tmp.append(dataMaterials[x])
                                y += 1
                            if(y==2):
                                y=0
                                dp.append(tmp)
                                tmp = [] 
                        for x in range(0, len(dp)):  
                            for y in range(0, len(dp[x])):
                                if (y==1):
                                    ProductsAddMaterialsReg = ProductsAddMaterials(
                                        ProductID = ProductsReg,
                                        MaterialID = Materials.objects.get(id = dp[x][0]),
                                        Quantity = dp[x][y],
                                    )

                                    ProductsAddMaterialsReg.save()                        

                    return redirect("/conf/products/#23")
                except:
                    # traceback.print_exc()  
                    return redirect("/conf/products/#21")
            else:
                return render(request, '403.html')

class modProducts(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_products':
                    pFlag = True
            if pFlag or request.user.is_staff:                               
                cntxProducts = Products.objects.get(id = self.kwargs['idProduct'])
                cntxMaterials = Materials.objects.filter(Block = True)
                cntxAddMaterials = ProductsAddMaterials.objects.filter(ProductID = self.kwargs['idProduct'])

                cntx = {
                    'user': request.user,
                    'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                    'Name':cntxProducts.Name,
                    'Description':cntxProducts.Description,
                    'Block':cntxProducts.Block,
                    'cntxMaterials': cntxMaterials,
                    'cntxAddMaterials': cntxAddMaterials
                    }
                return render(request, 'ConfProducts/modProducts.html', cntx)
            else:
                return render(request, '403.html')
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_products':
                    pFlag = True
            if pFlag or request.user.is_staff:
            
                cntxProducts = Products.objects.get(id = self.kwargs['idProduct'])

                cntxProducts.Name = request.POST.get('Name')
                cntxProducts.Description = request.POST.get('Description')

                if request.POST.get('Active')=='on': 
                    cntxProducts.Block = True
                else:
                    cntxProducts.Block = False

                try:
                    cntxProducts.save() 
                    ProductsAddMaterials.objects.filter(ProductID = self.kwargs['idProduct']).delete()
                    if(request.POST.get('input_dataMaterials') != ''):
                        dp = []
                        tmp = []
                        y = 0 
                        dataMaterials = request.POST.get("input_dataMaterials").split(",")
                        print(dataMaterials)
                        for x in range(0, len(dataMaterials)):
                            if (y<2):                         
                                tmp.append(dataMaterials[x])
                                y += 1
                            if(y==2):
                                y=0
                                dp.append(tmp)
                                tmp = [] 
                        for x in range(0, len(dp)):  
                            for y in range(0, len(dp[x])):
                                if (y==1):
                                    ProductsAddMaterialsReg = ProductsAddMaterials(
                                        ProductID = Products.objects.get(id = self.kwargs['idProduct']),
                                        MaterialID = Materials.objects.get(id = dp[x][0]),
                                        Quantity = dp[x][y],
                                    )

                                    ProductsAddMaterialsReg.save() 

                    return redirect('/conf/products/mod/'+str(cntxProducts.id)+'/#23')
                except:
                    return redirect('/conf/products/mod/'+str(cntxProducts.id)+'/#21')

            else:
                return render(request, '403.html')

class delProducts(DeleteView):
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
                        ProductsAddMaterials.objects.filter(ProductID = request.GET.get('productID')).delete()
                        Products.objects.get(id = request.GET.get('productID')).delete()                        
                        request.session["saveStatus"] = 1
                    except:
                        # traceback.print_exc()  
                        request.session["saveStatus"] = 0

                    cntxAjax = {
                        'status': request.session["saveStatus"]
                    }
                    return JsonResponse(cntxAjax)

                if (request.session["saveStatus"] == 1):
                    return redirect('/conf/products/#22')
                else:
                    return redirect('/conf/products/#21')

            else:
                return render(request, '403.html')