"""Stigma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

from Login.views import loginView, Index, logoutView, listUser, addUser, modUser, delUser, cpUser



urlpatterns = [

    path('', loginView.as_view()),
    path('admin/', admin.site.urls),
    path('index/', Index.as_view()),
    path('logout/', logoutView.as_view()),
    # -------------------------------------------------------------------------------------------USERS
    path('users/', listUser.as_view()), 
    path('users/add/', addUser.as_view()),
    re_path(r'^users/mod/(?P<idUser>(\d+))/', modUser.as_view(), name='modUser'),
    path('users/del/', delUser.as_view()), 
    re_path(r'^users/cp/(?P<idUser>(\d+))/', cpUser.as_view(), name='cpUser'),

    # -------------------------------------------------------------------------------------------Conf
    path('conf/', include('Conf.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler400 = error400 #bad_reques
# handler403 = error403 #permission_denied
# handler404 = error404 #page_not_found
# handler500 = error500 #server_error
