# Generated by Django 2.2.6 on 2020-01-12 15:20

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200106_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, null=True, srid=4326),
        ),
    ]
