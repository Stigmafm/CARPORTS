# Generated by Django 3.2.4 on 2021-07-17 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conf', '0019_auto_20210716_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='runs',
            name='Reschedule',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='runs',
            name='Status',
            field=models.CharField(blank=True, default='New', max_length=100, null=True),
        ),
    ]