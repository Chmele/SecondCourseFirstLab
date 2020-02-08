from django.db import models

class DictStreetOperations(models.Model):
    name = models.CharField('Назва операції',max_length = 100, null=True)
    description = models.CharField('Опис операції',max_length = 100, null=True)

    def __str__(self):
        return self.description

    class Meta:

        db_table = 'dit_dict_street_operations'
        verbose_name = 'Тип операції'
        verbose_name_plural = 'Словник типів операцій'



class DictStreetGeomType(models.Model):
    name = models.CharField('Тип геометрії',max_length = 100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:

        db_table = 'dit_dict_street_geom_type'
        verbose_name = 'Тип геометрії'
        verbose_name_plural = 'Словник типів геометрій'


class DictStreetTopocode(models.Model):
    name = models.CharField('Топокод',max_length = 100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:

        db_table = 'dit_dict_street_topocode'
        verbose_name = 'Топокод'
        verbose_name_plural = 'Словник топокодів'


class DictDistricts(models.Model):
    name = models.CharField('Назва району',max_length = 100, blank=True, null=True)
    # topocode = models.ForeignKey(DictStreetTopocode, models.DO_NOTHING, blank=True, null=True)
    # geom_type = models.ForeignKey(DictStreetGeomType, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:

        db_table = 'dit_dict_districts'
        verbose_name = 'Район'
        verbose_name_plural = 'Словник районів'


class DictStreetTract(models.Model):
    name = models.CharField('Тип тракту',max_length = 100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:

        db_table = 'dit_dict_street_tract'
        verbose_name = 'Тип тракту'
        verbose_name_plural = 'Словник типів тракту'


class DictStreetType(models.Model):
    name = models.CharField('Тип вулиці',max_length= 100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:

        db_table = 'dit_dict_street_type'
        verbose_name = 'Тип Вулиці'
        verbose_name_plural = 'Словник типів вулиць'

class DictBalanceHolder(models.Model):
    name = models.TextField('Назва балансоутримувача', blank=True, null=True)
    class Meta:
        db_table = 'dit_dict_balance_holder'