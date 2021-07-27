from django.shortcuts import render, redirect
from django.views.generic import FormView
# from Root.Session.forms.Login import LoginForm
from django.contrib.auth import authenticate, login, logout
from Login.models import auth_user_extend

# Create your views here.


class loginView(FormView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/index/')
        else:
           return render(request, 'Login/Login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # request.session["user"] = username
                home = auth_user_extend.objects.get(AuthUserID=user.id)
                #print (home.UrlHome)
                return redirect(home.UrlHome)
                # return redirect('/index/')
            else:
                return render(request, 'Login/LoginDU.html')
                # return redirect('/')
        else:
            return render(request, 'Login/LoginNA.html')
            # return redirect('/')

class logoutView(FormView):
    def get(self, request):
        logout(request)
        return redirect('/')