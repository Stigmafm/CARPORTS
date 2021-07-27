
import sys, traceback, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from Conf.models import Products, ProductsAddMaterials, Carports, Runs, RunsDetail, Staff
from django.contrib.auth.models import User
from Login.models import auth_user_extend

class mainRunReport(ListView): 
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
                cntxStaff = Staff.objects.filter().values()  
                cntxHistoryRuns = Runs.objects.filter(Q(ReadyRun = True) & Q(ProcessRun = True)).values().order_by('CreateDateTime')                

                for x in range(0, len(cntxHistoryRuns)):
                    cntxAsignedRuns = RunsDetail.objects.filter(RunID = cntxHistoryRuns[x]['id']).values().count()  
                    cntxSchedulerName = User.objects.get(id = cntxHistoryRuns[x]['Scheduler_id']) 
                    cntxHistoryRuns[x].update({'SchedulerName': str(cntxSchedulerName.first_name)+ str(' ') + str(cntxSchedulerName.last_name)})   
                    cntxHistoryRuns[x].update({'cntxAsignedRuns': cntxAsignedRuns})     
 
                cntx = {
                    'user': request.user,
                    'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                    'cntxStaff': cntxStaff,
                    'cntxHistoryRuns': cntxHistoryRuns,                    
                }

                return render(request, "ClientReports/mainRunReport.html", cntx)
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
                        cntxCarports = Carports.objects.filter().values()  
                        dataC = []
                        for x in range(0, len(cntxCarports)):                            
                            cntxCarport = Products.objects.get(id = cntxCarports[x]['ProductID_id'])
                            # totalC = Carports.objects.filter().values().count()
                            totalperC = Carports.objects.filter(ProductID = cntxCarports[x]['ProductID_id']).values().count()
                            dataC.append({'Carport':cntxCarport.Name, 'Quantity':totalperC})

                        repetido = []
                        unico = []
                        unico2 = []   

                        for x in range(0, len(dataC)):  
                            if(dataC[x]['Carport'] not in unico ):
                                unico.append(dataC[x]['Carport'])
                                unico2.append({'Carport':dataC[x]['Carport'], 'Quantity':dataC[x]['Quantity']})
                            else:
                                if(dataC[x]['Carport'] not in repetido):
                                    repetido.append(dataC[x]['Carport'])                                    
                                else:
                                    repetido.append(dataC[x]['Carport'])   

                        cntxAjax = {
                            'dataC': unico2
                        }
                        return JsonResponse(cntxAjax)                                
                
                #     traceback.print_exc()  
                return redirect("/conf/mainCorridas/")
            else:
                return render(request, '403.html')