from datetime import datetime, date
from dictionaries.models import *
from .models import *
from django.db.models import Q
import django.utils
import datetime
#GERMANYUK COMMENT
from django.contrib.gis.db import models

import os
#django.utils.timezone.now
class StreetAlternativeName(models.Model):
    name = models.CharField('Назва вулиці', max_length= 100, blank=False, null=False, default="")
    street = models.ForeignKey("Street", models.DO_NOTHING, blank=False, null=False, default=1)

    class Meta:

        db_table = 'dit_street_alternative_name'
        verbose_name = 'Альтернативна назва вулиці'
        verbose_name_plural = 'Альтернативні назви вулиць'

    def str(self):
        return self.name

class DocumentsStreet(models.Model):
    name = models.ForeignKey(DictStreetOperations, models.DO_NOTHING, blank=False, null=True, verbose_name='Назва документу', default=1)
    document = models.FileField( upload_to='files/', verbose_name='Документ')
    date = models.DateField('Дата затвердження документу', blank=False, null=True, default=django.utils.timezone.now)
    path_pdf = models.TextField('Шлях до PDF', blank=True, null=True, default="")
    pub_date = models.DateField('Дата додавання документу', blank=False, null=True, default=datetime.date.today)


    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Таблиця документів'
        db_table = 'dit_documents_street'


    def origin_name(self):
        return os.path.basename(str(self.document))

class OperationSegment(models.Model):
    old = models.ForeignKey('Segment', models.DO_NOTHING, related_name='old', db_column='old', blank=True, null=True, verbose_name='Старий сегмент')
    new = models.ForeignKey('Segment', models.DO_NOTHING, related_name='new', db_column='new', blank=True, null=True, verbose_name='Новий сегмент')
    date = models.DateField('Дата проведення операції над сегментом', blank=False, null=False, default=django.utils.timezone.now)
    document = models.ForeignKey(DocumentsStreet, models.DO_NOTHING, blank=False, null=False, default=1)

    class Meta:
        verbose_name = 'Операція над сегментом'
        verbose_name_plural = 'Операції над сегментами'
        db_table = 'dit_operation_segment'


class OperationSegmentStreet(models.Model):
    old = models.ForeignKey('SegmentStreet', models.DO_NOTHING, related_name='old', db_column='old', blank=True, null=True, verbose_name='Старий зв\'язок')
    new = models.ForeignKey('SegmentStreet', models.DO_NOTHING, related_name='new', db_column='new', blank=True, null=True, verbose_name='Новий зв\'язок')
    date = models.DateField('Дата проведення операції над парою вулиця-сегмент', blank=False, null=False, default=django.utils.timezone.now)
    document = models.ForeignKey(DocumentsStreet, models.DO_NOTHING, blank=False, null=False, default=1)

    class Meta:
        verbose_name = 'Операція над проведенням зв\'язку сегмент-вулиця'
        verbose_name_plural = 'Операції над проведенням зв\'язку сегмент-вулиця'
        db_table = 'dit_operation_segment_street'


class OperationStreet(models.Model):
    old = models.ForeignKey('Street', models.DO_NOTHING, related_name='old', db_column='old', blank=True, null=True, verbose_name='Стара вулиця')
    new = models.ForeignKey('Street', models.DO_NOTHING, related_name='new', db_column='new', blank=True, null=True, verbose_name='Нова вулиця')
    date = models.DateField('Дата проведення операції над вулицею', blank=False, null=True, default=django.utils.timezone.now)
    document = models.ForeignKey(DocumentsStreet, models.DO_NOTHING, blank=False, null=True, default=1)

    class Meta:
        verbose_name = 'Операція над вулицею'
        verbose_name_plural = 'Операції над вулицями'
        db_table = 'dit_operation_street'


class Segment(models.Model):
    stream_amount = models.IntegerField('Кількість потоків', blank=True, null=True)
    district = models.ForeignKey(DictDistricts, models.DO_NOTHING, blank=True, null=True)
    road_index = models.CharField('Індекс дороги', max_length=100, blank=True, null=True)
    width = models.FloatField('Ширина дороги(м)', blank=True, null=True)
    cover_type = models.CharField('Тип покриття', max_length=100, blank=True, null=True)
    balance_holder = models.ForeignKey(DictBalanceHolder, models.DO_NOTHING, blank=True, null=True)
    tract_mtz = models.ForeignKey(DictStreetTract, models.DO_NOTHING, blank=True, null=True)
    operation = models.ManyToManyField('self', through='OperationSegment', symmetrical=False)
    geom = models.MultiLineStringField(null=True, blank=True, dim=2, srid=4326)

    class Meta:

        db_table = 'dit_segment'
        verbose_name = 'Сегмент'
        verbose_name_plural = 'Перелік сегментів'

    def __str__(self):
        return "id: " + str(self.id) + " " #+ self.type.name


    def getStreet(self, date=date.today()):
        street = Street.objects.filter(
            Q(segmentstreet__segment__id=self.id),
            Q(segmentstreet__date_start__lte = date)|Q(segmentstreet__date_start=None),
            Q(segmentstreet__date_end__gt = date)|Q(segmentstreet__date_end=None),
        )
        return street

        
    @staticmethod
    def free_segments():
        not_free_id = SegmentStreet.objects.values('segment').distinct()
        segment_list = Segment.objects.exclude(id__in=not_free_id)
        return segment_list #render(request, 'main/detail.html', {'free_segments': segment_list})

class Street(models.Model):
    name = models.CharField('Назва вулиці', max_length= 100, blank=True, null=True)
    prev_id = models.IntegerField('Попередній ID', blank=True, null=True)
    topocode = models.ForeignKey(DictStreetTopocode, models.DO_NOTHING, blank=True, null=True)
    description = models.CharField('Опис вулиці', max_length= 100, blank=True, null=True)
    type = models.ForeignKey(DictStreetType, models.DO_NOTHING, blank=True, null=True)
    geom_type = models.ForeignKey(DictStreetGeomType, models.DO_NOTHING, blank=True, null=True)
    significance = models.CharField('Значення', max_length= 100, blank=True, null=True)
    segments = models.ManyToManyField(Segment, through='SegmentStreet')
    operation = models.ManyToManyField('self', through='OperationStreet', symmetrical=False)

    class Meta:

        db_table = 'dit_street'
        verbose_name = 'Вулиця'
        verbose_name_plural = 'Перелік вулиць'

    def __str__(self):
        return self.name

    def count_segments_by_date(self, date = date.today()):
        segments = Segment.objects.filter(
            Q(street__id=self.id),
            Q(segmentstreet__date_start__lte = date)|Q(segmentstreet__date_start=None),
            Q(segmentstreet__date_end__gt = date)|Q(segmentstreet__date_end=None),
        )
        return segments.count();

    # !!not tested
    def getDistricts(self, date = date.today):
        segments = Segment.objects.filter(
            Q(street__id=self.id),
            Q(segmentstreet__date_start__lte = date)|Q(segmentstreet__date_start=None),
            Q(segmentstreet__date_end__gt = date)|Q(segmentstreet__date_end=None),
        )
        districts = []
        for segment in segments:
            districts.append(segment.district)
        
        return districts.distinct()

class SegmentStreet(models.Model):
    street = models.ForeignKey(Street, models.DO_NOTHING, blank=False, null=False, default=1)
    segment = models.ForeignKey(Segment, models.DO_NOTHING, blank=False, null=False, default=1)
    date_start = models.DateField('Дата початку', blank=True, null=True)
    date_end = models.DateField('Дата кінця', blank=True, null=True)
    operation = models.ManyToManyField('self', through='OperationSegmentStreet', symmetrical=False)

    class Meta:

        db_table = 'dit_segment_street'
        verbose_name = "Зв'язок між вулицею та сегментом"
        verbose_name_plural = "Зв'язки між вулицями та сегментами"

    def __str__(self):
        return "Вулиця: " + str(self.street) + " Сегмент: " + str(self.segment)
