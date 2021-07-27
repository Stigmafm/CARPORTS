from django.db import models
from django.contrib.auth.models import User

class auth_user_extend(models.Model):
    AuthUserID = models.OneToOneField(User,  null=True, blank=True, on_delete=models.CASCADE, db_column='AuthUserID')
    UrlHome = models.CharField(max_length=100, null=False, blank=False, default='/')
    Image = models.TextField(null=True, blank=True)
    Position = models.CharField(max_length=100, null=True, blank=True)
    Department = models.CharField(max_length=100, null=True, blank=True)
    Block = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        app_label = 'Login'
        db_table = 'auth_user_extend'

    