# Generated by Django 3.2.4 on 2021-07-14 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conf', '0017_runs_readyrun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runs',
            name='RunNumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]