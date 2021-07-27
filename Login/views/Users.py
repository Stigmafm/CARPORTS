import traceback, datetime

import base64
import os.path

# from io import BytesIO

from django.contrib.auth.models import User, Group, Permission, ContentType
from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView, CreateView, ListView, DeleteView, UpdateView

from django.http import JsonResponse

# from PIL import Image
# from django.core.files.storage import FileSystemStorage
# from django.conf import settings

# from Root.Session.forms.Authentication import UserForm, GroupForm, PermissionForm
# from MES.Conf.MESModeling.models import sWarehouseLocation
from Login.models import auth_user_extend

class listUser(ListView):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_user':
                    pFlag = True
            if pFlag or request.user.is_staff:
                # request.session["badCP"]="False"
                cntx = {
                    'user': request.user,
                    'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                    'users': User.objects.all(),
                }
                return render(request, 'Users/listUser.html', cntx)
            else:
                return render(request, '403.html')

class addUser(CreateView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_user':
                    pFlag = True
            if pFlag or request.user.is_staff:
                cntx = {
                    # 'system':request.session["system"],
                    # 'systemMin':request.session["systemMin"],
                    'user': request.user,
                    'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                    'permission': Permission.objects.all(),
                    'group': Group.objects.all(),
                }
               
                return render(request, 'Users/addUser.html', cntx)
            else:
                return render(request, '403.html')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.add_user':
                    pFlag = True
            if pFlag or request.user.is_staff:

                if request.is_ajax():
                    username = request.POST.get('username')
                    #print username
                    cntxAjax = {
                        'is_taken': User.objects.filter(username__iexact=username).exists()
                    }
                    return JsonResponse(cntxAjax)
                else: 

                    # if request.FILES:
                    #     imgUp = request.FILES['Image']
                    #     fs = FileSystemStorage()
                    #     filename = fs.save('Session/Temp/00', imgUp)
                    #     #uploaded_file_url = fs.url(filename)

                    #     media = os.path.join(settings.MEDIA_ROOT)
                        
                    #     image = Image.open(os.path.join(media, filename))

                    #     img_buffer = BytesIO()
                    #     image.save(img_buffer, format="png")
                    #     img_str = base64.b64encode(img_buffer.getvalue()).decode()
                    
                    #     fs.delete('Session/Temp/00')
                    # else:
                    #     img_str = None

                    if request.POST.get('is_superuser')=='on': 
                        isu = True
                    else:
                        isu = False

                    if request.POST.get('is_staff')=='on': 
                        isst = True
                    else:
                        isst = False

                    if request.POST.get('is_active')=='on':
                       isa = True
                    else:
                        isa = False

                    userReg = User(
                        username = request.POST.get('username'),
                        email = request.POST.get('email'),
                        password = request.POST.get('password1'),
                        is_superuser = isu,
                        is_staff = isst,
                        is_active = isa,
                        first_name = request.POST.get('first_name'),
                        last_name =  request.POST.get('last_name'),
                        date_joined = datetime.datetime.now()
                    )

                    try:
                        userReg.save()

                        userReg.set_password( request.POST.get('password1'))
                        userReg.save()

                        # gp = request.POST.getlist('gpTo[]')
                        # perm = request.POST.getlist('permTo[]')

                        # for p in perm:
                        #     userReg.user_permissions.add(Permission.objects.get(id=p))
                        # for g in gp:
                        #     userReg.groups.add(Group.objects.get(id=g))

                        # userReg.save() 
                    
                        if (request.POST.get('UrlHome') == '' or request.POST.get('UrlHome') == None):
                            url = '/'
                        else:
                            url = request.POST.get('UrlHome')

                        userExtendReg = auth_user_extend(                                                                    
                            UrlHome = url,
                            # Image = img_str,
                            Position = request.POST.get('Position'),
                            # Department = request.POST.get('Department'),
                        )
                        userExtendReg.save()           

                        usExt = auth_user_extend.objects.get(id=userExtendReg.id)
                        usExt.AuthUserID = User.objects.get(id=userReg.id)  
                        usExt.save()

                        return redirect("/users/#23")
                    except:
                        return redirect("/users/#21")
            else:
                return render(request, '403.html')

class modUser(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_user':
                    pFlag = True
            if pFlag or request.user.is_staff:
                               
                us = User.objects.get(id=self.kwargs['idUser'])
                usExt = auth_user_extend.objects.get(AuthUserID=self.kwargs['idUser'])

                cntx = {
                        'user': request.user,
                        'userex': auth_user_extend.objects.get(AuthUserID=request.user.id),
                        'username':us.username,
                        'first_name':us.first_name,
                        'last_name':us.last_name,
                        'email':us.email,
                        'is_superuser':us.is_superuser,
                        'is_staff':us.is_staff,
                        'is_active':us.is_active,
                        'us': us, 
                        'usExt': usExt, 
                    }
                return render(request, 'Users/modUser.html', cntx)
            else:
                return render(request, '403.html')
                
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_user':
                    pFlag = True
            if pFlag or request.user.is_staff:
                # if request.FILES:
                #     imgUp = request.FILES['Image']
                #     fs = FileSystemStorage()
                #     filename = fs.save('Session/Temp/00', imgUp)
                #     #uploaded_file_url = fs.url(filename)
                        
                #     media = os.path.join(settings.MEDIA_ROOT)
                        
                #     image = Image.open(os.path.join(media, filename))

                #     img_buffer = BytesIO()
                #     image.save(img_buffer, format="png")
                #     img_str = base64.b64encode(img_buffer.getvalue()).decode()
                    
                #     fs.delete('Session/Temp/00')
                # else:
                #     img_str = None
            
                us = User.objects.get(id=self.kwargs['idUser'])
                
                usExt = auth_user_extend.objects.get(AuthUserID=self.kwargs['idUser'])
                
                usExt.AuthUserID = User.objects.get(id=self.kwargs['idUser'])
                usExt.UrlHome =  request.POST.get('UrlHome')
                # usExt.Image = img_str
                usExt.Position =  request.POST.get('Position')
                # usExt.Department =  request.POST.get('Department')
                
                usExt.save()
                
                # gp = request.POST.getlist('gpTo[]')
                # perm = request.POST.getlist('permTo[]')

                us.username = request.POST.get('username')
                us.first_name = request.POST.get('first_name')
                us.last_name = request.POST.get('last_name')
                us.email = request.POST.get('email')

                if request.POST.get('is_superuser')=='on': 
                    us.is_superuser = True
                else:
                    us.is_superuser = False

                if request.POST.get('is_staff')=='on': 
                    us.is_staff = True

                else:
                    us.is_staff = False

                if request.POST.get('is_active')=='on':
                    us.is_active = True
                else:
                    us.is_active = False

                try:
                    us.save()
               
                    # us.user_permissions.clear()
                    # us.groups.clear()

                    # for p in perm:
                    #     us.user_permissions.add(Permission.objects.get(id=p))
                    # for g in gp:
                    #     us.groups.add(Group.objects.get(id=g))                    
                    return redirect('/users/mod/'+str(us.id)+'/#23')
                    # return redirect('/users/mod/'+str(us.id)+'/#23')
                except:
                    return redirect('/users/mod/'+str(us.id)+'/#21')

            else:
                return render(request, '403.html')

class delUser(DeleteView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.del_user':
                    pFlag = True
            if pFlag or request.user.is_staff:
                if request.is_ajax():
                    try:
                        #auth_user_extend.objects.get(AuthUserID=request.GET.get('user')).delete()
                        User.objects.get(id=request.GET.get('user')).delete()                        
                        request.session["saveStatus"] = 1
                    except:
                        traceback.print_exc()  
                        request.session["saveStatus"] = 0

                    cntxAjax = {
                        'status': request.session["saveStatus"],
                    }
                    return JsonResponse(cntxAjax)

                if (request.session["saveStatus"] == 1):
                    return redirect('/users/#22')
                else:
                    return redirect('/users/#21')

            else:
                return render(request, '403.html')

class cpUser(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_user':
                    pFlag = True
            if pFlag or request.user.is_staff:
                us = User.objects.get(id=self.kwargs['idUser'])
                cntx = {
                        'user': request.user,
                        'username':us.username,
                        'first_name':us.first_name,
                        'last_name':us.last_name,
                        'email':us.email,
                        'us':us
                    }                
                return render(request, 'Users/cpUser.html', cntx)
            else:
                return render(request, '403.html')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html')
        else:
            pFlag = False
            perms = request.user.get_all_permissions()
            for prm in perms:
                if prm == 'auth.change_user':
                    pFlag = True
            if pFlag or request.user.is_staff:
                us = User.objects.get(id=self.kwargs['idUser'])                                            
                try:
                    us.set_password( request.POST.get('password1'))
                    us.save()
                    return redirect('/users/mod/'+str(us.id)+'/#23')
                except:
                    #traceback.print_exc()            
                    return redirect('/users/mod/'+str(us.id)+'/#21')
            else:
                return render(request, '403.html')
