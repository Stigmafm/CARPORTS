# Generated by Django 3.2.4 on 2021-07-11 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conf', '0012_carports_certification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carports',
            name='Certification',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]