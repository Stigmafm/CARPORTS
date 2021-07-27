from django.db import models
from django.contrib.auth.models import User
# from django.db.models.fields import IntegerField
# from django.db.models.query_utils import Q

# Create your models here.

class Materials(models.Model):
    Name = models.CharField(max_length=100, null=False, blank=False)
    Description = models.CharField(max_length=500, null=True, blank=True)
    Sizes = models.CharField(max_length=5, null=True, blank=True)
    Dependent = models.BooleanField(null=False, blank=False, default=False)
    Block = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        app_label = 'Conf'
        db_table = 'Materials'
    
    def __str__(self):
        return '{}'.format(self.Name)

class Staff(models.Model):
    Name = models.CharField(max_length=100, null=False, blank=False)
    Description = models.CharField(max_length=500, null=True, blank=True)
    Block = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        app_label = 'Conf'
        db_table = 'Staff'
    
    def __str__(self):
        return '{}'.format(self.Name)

class Products(models.Model):
    Name = models.CharField(max_length=100, null=False, blank=False)
    Description = models.CharField(max_length=500, null=True, blank=True)
    Block = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        app_label = 'Conf'
        db_table = 'Products'
    
    def __str__(self):
        return '{}'.format(self.Name)

class ProductsAddMaterials(models.Model):
    ProductID = models.ForeignKey('Products', null=True, blank=True, on_delete=models.SET_NULL, db_column='ProductID')
    MaterialID = models.ForeignKey('Materials', null=True, blank=True, on_delete=models.SET_NULL, db_column='MaterialID')
    Quantity = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)

    class Meta:
        app_label = 'Conf'
        db_table = 'ProductsAddMaterials'
    
    def __str__(self):
        return '{}'.format(self.Quantity)

class Carports(models.Model):
    Customer = models.CharField(max_length=100, null=True, blank=True)
    State = models.CharField(max_length=100, null=True, blank=True)
    City = models.CharField(max_length=100, null=True, blank=True)
    Address = models.CharField(max_length=100, null=True, blank=True)
    ZipCode = models.CharField(max_length=100, null=True, blank=True)
    Telephone = models.CharField(max_length=100, null=True, blank=True)
    ProductID = models.ForeignKey('Products', null=True, blank=True, on_delete=models.SET_NULL, db_column='ProductID')
    Width = models.IntegerField(null=False, blank=False)
    Length = models.IntegerField(null=False, blank=False)
    Heigth = models.IntegerField(null=False, blank=False)
    Gauge = models.IntegerField(null=False, blank=False)
    Certification = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        app_label = 'Conf'
        db_table = 'Carports'

    def __str__(self):
        return '{}'.format(self.ProductID.Name)

class Runs(models.Model):
    RunNumber = models.CharField(max_length=50, null=True, blank=True)
    CreateDateTime = models.DateTimeField(null=False, blank=False) 
    CargoDay = models.DateTimeField(null=True, blank=True) 
    InstallationDay = models.DateTimeField(null=True, blank=True) 
    Installer = models.CharField(max_length=100, null=True, blank=True)
    Scheduler = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, db_column='Scheduler')
    State = models.CharField(max_length=100, null=True, blank=True)
    NumberofCarports = models.IntegerField(null=False, blank=False, default=0)
    Status = models.CharField(max_length=100, null=True, blank=True, default='New') 
    ReadyRun = models.BooleanField(null=False, blank=False, default=False)
    ProcessRun = models.BooleanField(null=False, blank=False, default=False)    
    Reschedule = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        app_label = 'Conf'
        db_table = 'Runs'

    def __str__(self):
        return '{}'.format(self.RunNumber)

class RunsDetail(models.Model):
    RunID = models.ForeignKey('Runs', null=True, blank=True, on_delete=models.SET_NULL, db_column='RunID')   
    CarportID = models.ForeignKey('Carports', null=True, blank=True, on_delete=models.SET_NULL, db_column='CarportID')   

    class Meta:
        app_label = 'Conf'
        db_table = 'RunsDetail'

    def __str__(self):
        return '{}'.format(self.RunID.RunNumber)


        