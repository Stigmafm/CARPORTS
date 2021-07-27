from django.conf.urls import url, include
from django.urls import path
from Conf.views import listMaterials, addMaterials, modMaterials, delMaterials
from Conf.views import listStaff, addStaff, modStaff, delStaff
from Conf.views import listProducts, addProducts, modProducts, delProducts
from Conf.views import mainCorridas, addRun, updateRun, closeRun, rescheduleRun, assignInstallerRun, finishRun, cancelRun
from Conf.views import mainCarports, deleteCarport
from Conf.views import mainRunReport



urlpatterns = [
    #------------------------------------------------------------------------------------------------------ MATERIALS
    path('materials/', listMaterials.as_view(), name='listMaterials'),
    path('materials/add', addMaterials.as_view(), name='addMaterials'),
    path('materials/mod/<int:idMaterial>/', modMaterials.as_view(), name='modMaterials'),
    path('materials/del', delMaterials.as_view(), name='delMaterials'),

    #------------------------------------------------------------------------------------------------------ PERSONAL
    path('staff/', listStaff.as_view(), name='listStaff'),
    path('staff/add', addStaff.as_view(), name='addStaff'),
    path('staff/mod/<idStaff>/', modStaff.as_view(), name='modStaff'),
    path('staff/del', delStaff.as_view(), name='delStaff'),

    #------------------------------------------------------------------------------------------------------ PRODUCTS
    path('products/', listProducts.as_view(), name='listProducts'),
    path('products/add', addProducts.as_view(), name='addProducts'),
    path('products/mod/<idProduct>/', modProducts.as_view(), name='modProducts'),
    path('products/del', delProducts.as_view(), name='delProducts'),
    
    #------------------------------------------------------------------------------------------------------ CORRIDAS
    path('mainCorridas/', mainCorridas.as_view(), name='mainCorridas'),
    path('mainCorridas/addRun', addRun.as_view(), name='addRun'),
    path('mainCorridas/updateRun/', updateRun.as_view(), name='updateRun'),
    path('mainCorridas/closeRun', closeRun.as_view(), name='closeRun'),
    path('mainCorridas/rescheduleRun', rescheduleRun.as_view(), name='rescheduleRun'),
    path('mainCorridas/assignInstallerRun', assignInstallerRun.as_view(), name='assignInstallerRun'),
    path('mainCorridas/finishRun', finishRun.as_view(), name='finishRun'),
    path('mainCorridas/cancelRun', cancelRun.as_view(), name='cancelRun'),

    #------------------------------------------------------------------------------------------------------ CARPORTS
    path('mainCarports/', mainCarports.as_view(), name='mainCarports'),
    path('mainCarports/deleteCarport', deleteCarport.as_view(), name='deleteCarport'),

    #------------------------------------------------------------------------------------------------------ REPORTS
    path('mainRunReport/', mainRunReport.as_view(), name='mainRunReport'),
    # path('mainCarports/deleteCarport', deleteCarport.as_view(), name='deleteCarport'),

]
