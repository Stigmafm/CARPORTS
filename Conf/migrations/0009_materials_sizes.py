# Generated by Django 3.2.4 on 2021-06-29 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conf', '0008_materials_dependent'),
    ]

    operations = [
        migrations.AddField(
            model_name='materials',
            name='Sizes',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]