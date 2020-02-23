from django.contrib.gis import admin
from django.db import models
from .models import *
from leaflet.admin import LeafletGeoAdminMixin
from import_export.admin import ImportExportModelAdmin

class SegmentStreetInline(admin.TabularInline):
    model = SegmentStreet
    autocomplete_fields = ['street', 'segment']
    extra = 0
    ordering = ('id',)
    # def get_queryset(self, request):
    #     return Segment.free_segments()

class OperationStreetInline(admin.TabularInline):
    model = OperationStreet
    autocomplete_fields = ['new', 'old']
    extra = 1
    ordering = ('id',)

class OperationSegmentStreetInline(admin.TabularInline):
    model = OperationSegmentStreet
    autocomplete_fields = ['new', 'old']
    extra = 1
    ordering = ('id',)

class OperationSegmentInline(admin.TabularInline):
    model = OperationSegment
    autocomplete_fields = ['new', 'old']
    extra = 1
    ordering = ('id',)


class StreetAlternativeNameInline(admin.TabularInline):
    model = StreetAlternativeName
    autocomplete_fields = ['street']
    extra = 1
    ordering = ('id',)

class SegmentsOfStreetInline(LeafletGeoAdminMixin, admin.StackedInline):
    model = SegmentStreet
    extra = 1
    ordering = ('id',)

class AdminStreet(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'description']
    fieldsets = [
        (None,               {'fields': ['name', 'description', 'significance']}),
        ('Дані з довідників', {'fields': ['type']}),
    ]
    search_fields = ['name', 'streetalternativename__name']
    list_filter = ['type', 'segmentstreet__segment__district']
    #ОСТОРОЖНО
    #inlines = (Street.free_segments(), StreetAlternativeNameInline,)
    inlines = (SegmentStreetInline, StreetAlternativeNameInline,)
    ordering = ('id',)

class AdminSegmentStreet(admin.ModelAdmin):
    search_fields = ['id']

class AdminOperationStreet(admin.ModelAdmin):
    list_display = ['date']
    autocomplete_fields = ['new', 'old']
    ordering = ('id',)

class AdminOperationSegmentStreet(admin.ModelAdmin):
    list_display = ['date']
    autocomplete_fields = ['new', 'old']
    ordering = ('id',)

class AdminOperationSegment(admin.ModelAdmin):
    list_display = ['date']
    search_fields = ['new', 'old']
    ordering = ('id',)

class AdminSegment(admin.OSMGeoAdmin, ImportExportModelAdmin):
    list_display = ['id', 'district']
    fieldsets = [
        (None,               {'fields': ['road_index', 'width', 'cover_type', 'geom']}),
        ('Дані з довідників', {'fields': ['district',  'balance_holder', 'tract_mtz']}),
    ]
    list_filter = ['district']
    search_fields = ['id']
    inlines = (SegmentStreetInline, )
    ordering = ('id',)

class AdminDocumentsStreet(admin.ModelAdmin):
    list_display = ['id', 'name']
    fieldsets = [
        (None,               {'fields': ['document', 'date']}),
        ('Дані з довідників', {'fields': ['name']}),
    ]
    list_filter = ['name']
    search_fields = ['id', 'name']
    inlines = ( OperationStreetInline, OperationSegmentInline, OperationSegmentStreetInline, )
    ordering = ('id',)


admin.site.register(Street, AdminStreet)
admin.site.register(SegmentStreet, AdminSegmentStreet)
admin.site.register(OperationStreet, AdminOperationStreet)
# admin.site.register(OperationSegmentStreet, AdminOperationSegmentStreet)
admin.site.register(OperationSegment, AdminOperationSegment)
admin.site.register(DocumentsStreet, AdminDocumentsStreet)
admin.site.register(StreetAlternativeName)
admin.site.register(Segment, AdminSegment)
admin.site.site_header = "UMSRA Admin"
admin.site.site_title = "UMSRA Admin Portal"
admin.site.index_title = "Welcome to UMSRA Researcher Portal"
