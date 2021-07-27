
from Conf.models.Materials import Materials, Products
import sys, traceback, datetime
from datetime import datetime, date, time, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from Conf.models import Products, ProductsAddMaterials, Carports, Runs, RunsDetail, Staff
from django.contrib.auth.models import User
from Login.models import auth_user_extend

class mainCorridas(ListView): 
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'Conf.view_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:  

                cntxStaff = Staff.objects.filter(Block = True).values()
                cntxOpenRun = Runs.objects.filter(ReadyRun = False).values()   
                cntxReadyRuns = Runs.objects.filter(Q(ReadyRun = True) & Q(ProcessRun = False)).values().order_by('CreateDateTime')   
                cntxRunsTop = Runs.objects.filter(ProcessRun = True).values().order_by('-CreateDateTime')[:10]   
                cntxCarports = Carports.objects.all() 

                for x in range(0, len(cntxOpenRun)):
                    # print(cntxOpenRun)
                    cntxAsignedRuns = RunsDetail.objects.filter(RunID = cntxOpenRun[x]['id']).values().count()   
                    cntxSchedulerName = User.objects.get(id = cntxOpenRun[x]['Scheduler_id']) 
                    cntxOpenRun[x].update({'SchedulerName': str(cntxSchedulerName.first_name)+ str(' ') + str(cntxSchedulerName.last_name)}) 
                    cntxOpenRun[x].update({'cntxAsignedRuns': cntxAsignedRuns}) 

                for x in range(0, len(cntxReadyRuns)):
                    cntxAsignedRuns = RunsDetail.objects.filter(RunID = cntxReadyRuns[x]['id']).values().count()  
                    cntxSchedulerName = User.objects.get(id = cntxReadyRuns[x]['Scheduler_id']) 
                    cntxReadyRuns[x].update({'SchedulerName': str(cntxSchedulerName.first_name)+ str(' ') + str(cntxSchedulerName.last_name)})   
                    cntxReadyRuns[x].update({'cntxAsignedRuns': cntxAsignedRuns})  

                for x in range(0, len(cntxRunsTop)):
                    cntxAsignedRuns = RunsDetail.objects.filter(RunID = cntxRunsTop[x]['id']).values().count()  
                    cntxSchedulerName = User.objects.get(id = cntxRunsTop[x]['Scheduler_id']) 
                    cntxRunsTop[x].update({'SchedulerName': str(cntxSchedulerName.first_name)+ str(' ') + str(cntxSchedulerName.last_name)})     
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
                if prm == 'auth.view_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:  
                if request.is_ajax():
                    if request.POST.get('operationNo') == '0':
                        data = []
                        cntxRun = Runs.objects.get(id = request.POST.get('RunID'))
                        cntxRunsDetails = RunsDetail.objects.filter(RunID = request.POST.get('RunID')).values()

                        for x in range(0, len(cntxRunsDetails)):
                            cntxCarport = Carports.objects.get(id = cntxRunsDetails[x]['CarportID_id'])
                            cntxRunsDetails[x].update({'Name': cntxCarport.ProductID.Name})
                            cntxRunsDetails[x].update({'Width': str(cntxCarport.Width)})
                            cntxRunsDetails[x].update({'Length': str(cntxCarport.Length)})
                            cntxRunsDetails[x].update({'Heigth': str(cntxCarport.Heigth)})
                            cntxRunsDetails[x].update({'Gauge': str(cntxCarport.Gauge)})
                            cntxRunsDetails[x].update({'Certification': str(cntxCarport.Certification)})
                            data.append([cntxCarport.ProductID.Name,cntxCarport.Customer,cntxCarport.Address,cntxCarport.City,cntxCarport.State,cntxCarport.Telephone])
                        # print(cntxRunsDetails)                      


                        cntxAjax = {
                            'RunNumber': cntxRun.RunNumber,
                            'Scheduler': str(cntxRun.Scheduler.first_name) + str(' ') + str(cntxRun.Scheduler.last_name),
                            'RunInstaller': cntxRun.Installer,
                            'RunCargoDay': cntxRun.CargoDay,
                            'RunState': cntxRun.State,
                            'RunStatus': cntxRun.Status,
                            'cntxRunsDetails': list(cntxRunsDetails),
                            'data': data
                        }
                        return JsonResponse(cntxAjax)                                
                
                #     traceback.print_exc()  
                return redirect("/conf/mainCorridas/")
            else:
                return render(request, '403.html')

class addRun(CreateView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:
                cntxStaff = Staff.objects.all()                

                cntx = {
                    'user': request.user,
                    'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                    'cntxStaff': cntxStaff
                }
               
                return render(request, 'ClientCorridas/addRun.html', cntx)
            else:
                return render(request, '403.html')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:  

                if(request.POST.get('select_staff') == 0 or request.POST.get('select_staff') == ''):
                    Intaller = 'Sin Asignar' 
                else:
                    Intaller = request.POST.get('select_staff')
                               
                RunsReg = Runs(
                    CreateDateTime = datetime.now(),
                    CargoDay = request.POST.get('CargoDayDate'),
                    InstallationDay = request.POST.get('InstallationDayDate'),
                    Installer = Intaller,
                    Scheduler = User.objects.get(id = request.POST.get('SchedulerID')),
                    State = request.POST.get('State'),
                    NumberofCarports = request.POST.get('NumberofCarports')
                )

                try:
                    RunsReg.save() 
                    # now = datetime.now()
                    # Day = str("{}".format(now.day))                    
                    # Month = str("{}".format(now.month))    
                    # today = Day.zfill(2) + Month.zfill(2) + str("{}".format(now.year))
                    runID = str(RunsReg.id)
                    # RunNumber = str(today) + str('-') + str(runID.zfill(4))
                    RunNumber = str(runID.zfill(5))
                    cntxRun = Runs.objects.get(id = RunsReg.id)
                    cntxRun.RunNumber = RunNumber
                    cntxRun.save()
                    # print(now)
                    # print("El día actual es {}".format(now.day))
                    # print("El mes actual es {}".format(now.month))
                    # print("El año actual es {}".format(now.year))
                    # print("La hora actual es {}".format(now.hour))
                    # print("El minuto actual es {}".format(now.minute))
                    # print("El segundo actual es {}".format(now.second))
                    # print(today)                  

                    return redirect("/conf/mainCorridas/#23")
                except:
                    traceback.print_exc()  
                    return redirect("/conf/mainCorridas/#21")
            else:
                return render(request, '403.html')

class updateRun(CreateView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:
                if(request.GET.get('RunID')):
                    cntxRuns = Runs.objects.get(id = request.GET.get('RunID')) 
                    cntxAsignedRuns = RunsDetail.objects.filter(RunID = cntxRuns.id).values().count() 
                    cntxAsignedCarportsRuns = RunsDetail.objects.filter(RunID = cntxRuns.id).values()
                    # print(cntxAsignedCarportsRuns)
                    for x in range(0, len(cntxAsignedCarportsRuns)):
                        cntxCarportName = Carports.objects.get(id = cntxAsignedCarportsRuns[x]['CarportID_id'])
                        # CarportSize = int(cntxCarportName.Width)

                        # print(cntxCarportName.ProductID.Name)
                        cntxAsignedCarportsRuns[x].update({'CarportName': str(cntxCarportName.ProductID.Name)})
                        cntxAsignedCarportsRuns[x].update({'Width': str(cntxCarportName.Width)})
                        cntxAsignedCarportsRuns[x].update({'Length': str(cntxCarportName.Length)})
                        cntxAsignedCarportsRuns[x].update({'Heigth': str(cntxCarportName.Heigth)})




                cntxStaff = Staff.objects.all()                

                cntx = {
                    'user': request.user,
                    'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                    'cntxRuns': cntxRuns,
                    'cntxAsignedRuns': cntxAsignedRuns,
                    'cntxAsignedCarportsRuns': cntxAsignedCarportsRuns
                }
               
                return render(request, 'ClientCorridas/updateRun.html', cntx)
            else:
                return render(request, '403.html')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:  

                if(request.POST.get('select_staff') == 0 or request.POST.get('select_staff') == ''):
                    Intaller = 'Sin Asignar' 
                else:
                    Intaller = request.POST.get('select_staff')
                               
                RunsReg = Runs(
                    CreateDateTime = datetime.now(),
                    CargoDay = request.POST.get('CargoDayDate'),
                    InstallationDay = request.POST.get('InstallationDayDate'),
                    Installer = Intaller,
                    State = request.POST.get('State')
                )

                try:
                    RunsReg.save() 
                    # now = datetime.now()
                    # Day = str("{}".format(now.day))                    
                    # Month = str("{}".format(now.month))    
                    # today = Day.zfill(2) + Month.zfill(2) + str("{}".format(now.year))
                    runID = str(RunsReg.id)
                    # RunNumber = str(today) + str('-') + str(runID.zfill(4))
                    RunNumber = str(runID.zfill(4))
                    cntxRun = Runs.objects.get(id = RunsReg.id)
                    cntxRun.RunNumber = RunNumber
                    cntxRun.save()
                    # print(now)
                    # print("El día actual es {}".format(now.day))
                    # print("El mes actual es {}".format(now.month))
                    # print("El año actual es {}".format(now.year))
                    # print("La hora actual es {}".format(now.hour))
                    # print("El minuto actual es {}".format(now.minute))
                    # print("El segundo actual es {}".format(now.second))
                    # print(today)                  

                    return redirect("/conf/mainCarports/")
                except:
                    traceback.print_exc()  
                    return redirect("/conf/mainCorridas/#21")
            else:
                return render(request, '403.html')

class closeRun(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:
                if request.is_ajax():
                    try:
                        if(RunsDetail.objects.filter(RunID = request.GET.get('RunID')).count() > 0 ):
                            cntxRun = Runs.objects.get(id = request.GET.get('RunID'))
                            cntxRun.ReadyRun = True
                            cntxRun.save()
                            StatusRun = 'Saved'                     
                            request.session["saveStatus"] = 1
                        else:
                            request.session["saveStatus"] = 0
                            StatusRun = 'NotCarports' 
                    except:
                        # traceback.print_exc()  
                        request.session["saveStatus"] = 0
                        StatusRun = 'NotSaved' 

                    cntxAjax = {
                        'status': request.session["saveStatus"],
                        'StatusRun': StatusRun
                    }
                    return JsonResponse(cntxAjax)

                if (request.session["saveStatus"] == 1):
                    return redirect('/conf/mainCorridas/#23')
                else:
                    return redirect('/conf/mainCorridas/#21')
            else:
                return render(request, '403.html')

class rescheduleRun(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:
                if request.is_ajax():
                    try:
                        cntxRun = Runs.objects.get(id = request.GET.get('RunID'))
                        cntxRun.CargoDay = request.GET.get('CargoDay')
                        cntxRun.InstallationDay = request.GET.get('InstallationDay')
                        countReschedule = int(cntxRun.Reschedule) + 1
                        cntxRun.Reschedule = countReschedule
                        cntxRun.Status = 'Reschedule-' + str(countReschedule)
                        cntxRun.save()                     
                        request.session["saveStatus"] = 1
                    except:
                        # traceback.print_exc()  
                        request.session["saveStatus"] = 0

                    cntxAjax = {
                        'status': request.session["saveStatus"],
                    }
                    return JsonResponse(cntxAjax)

                if (request.session["saveStatus"] == 1):
                    return redirect('/conf/mainCorridas/#23')
                else:
                    return redirect('/conf/mainCorridas/#21')
            else:
                return render(request, '403.html')

class assignInstallerRun(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:
                if request.is_ajax():
                    try:
                        cntxRun = Runs.objects.get(id = request.GET.get('RunID'))
                        cntxRun.Installer = request.GET.get('Installer')
                        cntxRun.save()                     
                        request.session["saveStatus"] = 1
                    except:
                        # traceback.print_exc()  
                        request.session["saveStatus"] = 0

                    cntxAjax = {
                        'status': request.session["saveStatus"],
                    }
                    return JsonResponse(cntxAjax)

                if (request.session["saveStatus"] == 1):
                    return redirect('/conf/mainCorridas/#23')
                else:
                    return redirect('/conf/mainCorridas/#21')
            else:
                return render(request, '403.html')

class finishRun(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:
                if request.is_ajax():                    
                    try:
                        if (Runs.objects.get(id = request.GET.get('RunID')).Installer == 'Sin Asignar'):
                            Installer = False
                            request.session["saveStatus"] = 0
                        else:
                            Installer = True
                            cntxRun = Runs.objects.get(id = request.GET.get('RunID'))
                            cntxRun.ProcessRun = True
                            cntxRun.save()                     
                            request.session["saveStatus"] = 1
                    except:
                        # traceback.print_exc()  
                        request.session["saveStatus"] = 0
                        Installer = False

                    cntxAjax = {
                        'status': request.session["saveStatus"],
                        'Installer': Installer
                    }
                    return JsonResponse(cntxAjax)

                if (request.session["saveStatus"] == 1):
                    return redirect('/conf/mainCorridas/#23')
                else:
                    return redirect('/conf/mainCorridas/#21')
            else:
                return render(request, '403.html')

class cancelRun(DeleteView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.delete_runs':
                    pFlag = True
            if pFlag or request.user.is_staff:
                if request.is_ajax():
                    try:
                        RunsDetail.objects.filter(RunID = request.GET.get('RunID')).delete()
                        Runs.objects.get(id = request.GET.get('RunID')).delete()                        
                        request.session["saveStatus"] = 1
                    except:
                        # traceback.print_exc()  
                        request.session["saveStatus"] = 0

                    cntxAjax = {
                        'status': request.session["saveStatus"]
                    }
                    return JsonResponse(cntxAjax)

                if (request.session["saveStatus"] == 1):
                    return redirect('/conf/mainCorridas/#22')
                else:
                    return redirect('/conf/mainCorridas/#21')
                # return redirect('/conf/mainCorridas/')
            else:
                return render(request, '403.html')