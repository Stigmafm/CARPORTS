
from Conf.models.Materials import Materials, Products
import sys, traceback, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from Conf.models import Products, ProductsAddMaterials, Carports, Runs, RunsDetail, Staff
from Login.models import auth_user_extend

class mainCarports(ListView): 
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'Conf.view_Carports':
                    pFlag = True
            if pFlag or request.user.is_staff:  
                if(Runs.objects.filter(ReadyRun = False).count() > 0):
                    if(request.GET.get('RunID')):
                        cntxProducts = Products.objects.filter(Block = True)
                        cntxRuns = Runs.objects.get(id = request.GET.get('RunID'))  
                        cntxAsignedRuns = RunsDetail.objects.filter(RunID = cntxRuns.id).values().count()                       
                        cntx = {
                            'user': request.user,
                            'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                            'cntxProducts': cntxProducts,
                            'cntxRuns': cntxRuns,
                            'cntxAsignedRuns': cntxAsignedRuns
                        }
                        return render(request, "ClientCarports/mainCarport.html", cntx)

                    else:
                        cntxOpenRun = Runs.objects.filter(Q(ReadyRun = False) & Q(Scheduler = request.user.id)).values()   
                        cntx = {
                            'user': request.user,
                            'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                            'cntxOpenRun': cntxOpenRun
                        }
                        return render(request, "ClientCarports/mainCarport.html", cntx)
                else:
                    cntxStaff = Staff.objects.filter().values()
                    cntxOpenRun = Runs.objects.filter(ReadyRun = False).values()   
                    cntxReadyRuns = Runs.objects.filter(Q(ReadyRun = True) & Q(ProcessRun = False)).values().order_by('CreateDateTime')   
                    cntxRunsTop = Runs.objects.filter(ProcessRun = True).values().order_by('-CreateDateTime')[:10]   

                    for x in range(0, len(cntxOpenRun)):
                        cntxAsignedRuns = RunsDetail.objects.filter(RunID = cntxOpenRun[x]['id']).values().count()    
                        cntxOpenRun[x].update({'cntxAsignedRuns': cntxAsignedRuns}) 

                    for x in range(0, len(cntxReadyRuns)):
                        cntxAsignedRuns = RunsDetail.objects.filter(RunID = cntxReadyRuns[x]['id']).values().count()    
                        cntxReadyRuns[x].update({'cntxAsignedRuns': cntxAsignedRuns})  

                    for x in range(0, len(cntxRunsTop)):
                        cntxAsignedRuns = RunsDetail.objects.filter(RunID = cntxRunsTop[x]['id']).values().count()    
                        cntxRunsTop[x].update({'cntxAsignedRuns': cntxAsignedRuns})  
                    
                    cntx = {
                        'user': request.user,
                        'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                        'cntxStaff': cntxStaff,
                        'cntxOpenRun': cntxOpenRun,
                        'cntxReadyRuns': cntxReadyRuns,
                        'cntxRunsTop': cntxRunsTop,
                    }
                    return render(request, "ClientCorridas/mainCorridas.html", cntx)    
            else:
                return render(request, '403.html')
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_Carports':
                    pFlag = True
            if pFlag or request.user.is_staff:

                CarportsReg = Carports(
                    Customer = request.POST.get('customerName'),
                    Address = request.POST.get('Address'),
                    City = request.POST.get('City'),
                    State = request.POST.get('State'),
                    ZipCode = request.POST.get('Zip_Code'),
                    Telephone = request.POST.get('Telephone'),
                    ProductID = Products.objects.get(id = request.POST.get('select_Products')),
                    Width = request.POST.get('Width'),
                    Length = request.POST.get('Length'),
                    Heigth = request.POST.get('Heigth'),
                    Gauge = request.POST.get('Gauge'),
                    Certification = request.POST.get('Certification')
                )

                try:
                    CarportsReg.save()
                    RunsDetailReg = RunsDetail(
                        CarportID = Carports.objects.get(id = CarportsReg.id),
                        RunID = Runs.objects.get(id = request.POST.get('input_RunActive'))
                    )
                    RunsDetailReg.save()

                    if (request.POST.get("saveFinish")):
                        cntxRun = Runs.objects.get(id = request.POST.get("input_RunActive"))
                        cntxRun.ReadyRun = True
                        cntxRun.save()
                        return redirect('/conf/mainCorridas/#23')                        
                    elif (request.POST.get("saveOther")):                        
                        return redirect('/conf/mainCarports/?RunID='+request.POST.get('input_RunActive'))
                    
                except:
                    # traceback.print_exc()                     
                    if (request.POST.get("saveFinish")):
                        return render(request, '/conf/mainCarports/#21')                       
                    elif (request.POST.get("saveOther")):                        
                        return render(request, '/conf/mainCarports/#21')
                        
                    # if request.POST.get('operationNo') == '1': 
                    #     print('ID Producto: ' + str(request.POST.get('ProductID')))  
                    #     # print('Width:' + str(request.POST.get('Width')))
                    #     # print('Length:' + str(request.POST.get('Length')))
                    #     # print('Heigth:' + str(request.POST.get('Heigth')))
                    #     cntxProducts = ProductsAddMaterials.objects.filter(ProductID = request.POST.get('ProductID')).values()

                    #     for x in range(0, len(cntxProducts)):
                    #         materialName = Materials.objects.get(id = cntxProducts[x]['MaterialID_id'])
                    #         # print(cntxProducts)
                    #         if (materialName.Dependent == True):
                    #             if(materialName.Sizes == 'W'):
                    #                 if(request.POST.get('Width') == '0' ):
                    #                     Size = '0'  
                    #                 else:
                    #                     Size = request.POST.get('Width')
                    #             elif(materialName.Sizes == 'L'):
                    #                 if(request.POST.get('Length') == '0' ):
                    #                     Size = '0'  
                    #                 else:
                    #                     Size = request.POST.get('Length')
                    #             elif(materialName.Sizes == 'H'):
                    #                 if(request.POST.get('Heigth') == '0' ):
                    #                     Size = '0'  
                    #                 else:
                    #                     Size = request.POST.get('Heigth')
                    #             else:
                    #                 Size = '0'                                    
                    #         else:
                    #             Size = '0'

                    #         if(request.POST.get('ProductID') == '1'):
                    #             # print('hola')
                    #             if (materialName.Name == 'Tornillos Washer'):
                    #                 cntxTornillosW = (5*5*4)
                    #                 cntxTornillosWPer = cntxTornillosW*0.1
                    #                 cntxTornillosW = round(cntxTornillosW + cntxTornillosWPer)
                    #                 # print(cntxTornillosW)
                    #                 cntxProducts[x].update({'Quantity': cntxTornillosW})
                    #             else:
                    #                 cntxProducts[x].update({'Quantity': cntxProducts[x]['Quantity']})
                                
                    #             if (materialName.Name == 'Tornillos sin Washer'):
                    #                 cntxTornillos = ((8*10)+(8*5)+(8*15))
                    #                 cntxTornillosPer = cntxTornillos*0.1
                    #                 cntxTornillos = round(cntxTornillos + cntxTornillosPer)
                    #                 # print(cntxTornillos)
                    #                 cntxProducts[x].update({'Quantity': cntxTornillos})
                    #             else:
                    #                 cntxProducts[x].update({'Quantity': cntxProducts[x]['Quantity']})

                    #         if(request.POST.get('ProductID') == '2'):
                    #             # print('hola')
                    #             if (materialName.Name == 'Box Trim'):
                    #                 cntxBoxTrim = (20/10)*2                                    
                    #                 cntxBoxTrimPer = cntxBoxTrim*0.1
                    #                 cntxBoxTrim = round(cntxBoxTrim + cntxBoxTrimPer)                                    
                    #                 # print(cntxTornillosW)
                    #                 cntxProducts[x].update({'Quantity': cntxBoxTrim})
                    #             else:
                    #                 cntxProducts[x].update({'Quantity': cntxProducts[x]['Quantity']})

                    #             if (materialName.Name == 'Tornillos Washer'):
                    #                 cntxTornillosW = (5*5*4)+(5*8)
                    #                 cntxTornillosWPer = cntxTornillosW*0.1
                    #                 cntxTornillosW = round(cntxTornillosW + cntxTornillosWPer)
                    #                 # print(cntxTornillosW)
                    #                 cntxProducts[x].update({'Quantity': cntxTornillosW})
                    #             else:
                    #                 cntxProducts[x].update({'Quantity': cntxProducts[x]['Quantity']})
                                
                    #             if (materialName.Name == 'Tornillos sin Washer'):
                    #                 cntxTornillos = ((8*10)+(8*15))
                    #                 cntxTornillosPer = cntxTornillos*0.1
                    #                 cntxTornillos = round(cntxTornillos + cntxTornillosPer)
                    #                 # print(cntxTornillos)
                    #                 cntxProducts[x].update({'Quantity': cntxTornillos})
                    #             else:
                    #                 cntxProducts[x].update({'Quantity': cntxProducts[x]['Quantity']})
                            
                    #         if(request.POST.get('ProductID') == '3'):
                    #             # print('hola')
                    #             if (materialName.Name == 'Ridge Cap-Trim'):
                    #                 cntxRidgeCapTrim = (20/10)
                    #                 cntxRidgeCapTrimPer = cntxRidgeCapTrim*0.1
                    #                 cntxRidgeCapTrim = round(cntxRidgeCapTrim + cntxRidgeCapTrimPer )
                    #                 # print(cntxTornillosW)
                    #                 cntxProducts[x].update({'Quantity': cntxRidgeCapTrim})
                    #             else:
                    #                 cntxProducts[x].update({'Quantity': cntxProducts[x]['Quantity']})

                    #             if (materialName.Name == 'Tornillos Washer'):
                    #                 cntxTornillosW = (3*4*14)+(10*5)
                    #                 cntxTornillosWPer = cntxTornillosW*0.1
                    #                 cntxTornillosW = round(cntxTornillosW + cntxTornillosWPer)
                    #                 # print(cntxTornillosW)
                    #                 cntxProducts[x].update({'Quantity': cntxTornillosW})
                    #             else:
                    #                 cntxProducts[x].update({'Quantity': cntxProducts[x]['Quantity']})
                                
                    #             if (materialName.Name == 'Tornillos sin Washer'):
                    #                 cntxTornillos = ((8*10)+(6*5*2)+(8*15))
                    #                 cntxTornillosPer = cntxTornillos*0.1
                    #                 cntxTornillos = round(cntxTornillos + cntxTornillosPer)
                    #                 # print(cntxTornillos)
                    #                 cntxProducts[x].update({'Quantity': cntxTornillos})
                    #             else:
                    #                 cntxProducts[x].update({'Quantity': cntxProducts[x]['Quantity']})

                    #         cntxProducts[x].update({'MName': materialName.Name})
                    #         cntxProducts[x].update({'Size': Size})

                    #     cntxAjax = {
                    #         'cntxProducts': list(cntxProducts)
                    #     }
                    #     return JsonResponse(cntxAjax)
                
                
                # return redirect('/conf/mainCarports/')  
            else:
                return render(request, '403.html')

class deleteCarport(DeleteView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.delete_carports':
                    pFlag = True
            if pFlag or request.user.is_staff:
                if request.is_ajax():
                    try:
                        RunsDetail.objects.get(CarportID = request.GET.get('CarportID')).delete()
                        Carports.objects.get(id = request.GET.get('CarportID')).delete()       
                        Status = 'Saved'
                    except:
                        # traceback.print_exc() 
                        Status = 'NotSaved'

                    cntxAjax = {
                        'Status': Status
                    }
                    return JsonResponse(cntxAjax)
                return redirect('/conf/mainCorridas/')
            else:
                return render(request, '403.html')