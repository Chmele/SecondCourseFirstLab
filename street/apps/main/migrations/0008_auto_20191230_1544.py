# Generated by Django 2.2.6 on 2019-12-30 13:44

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20191230_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, null=True, srid=100000),
        ),
    ]
