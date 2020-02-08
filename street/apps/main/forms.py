from django.contrib.gis import forms

from .models import *

class DocumentsStreetForm(forms.ModelForm):

    class Meta:
        model = DocumentsStreet
        fields = ('name', 'document', 'date',)

class StreetForm(forms.ModelForm):

    class Meta:
        model = Street
        fields = ('name', 'type',)

class OperationStreetForm(forms.ModelForm):

    class Meta:
        model = OperationStreet
        fields = ('date',)

class SegmentForm(forms.ModelForm):
    geom = forms.MultiLineStringField(widget=
        forms.OSMWidget(attrs={
            'map_width': 800,
            'map_height': 500,
            'default_lat': 50.45466,
            'default_lon': 30.5238,
            'default_zoom': 10}))
    class Meta:
        model = Segment
        fields = ('district', 'geom')

class SegmentChangeGeomForm(forms.ModelForm):
    geom = forms.MultiLineStringField(widget=
        forms.OSMWidget(attrs={
            'default_zoom': 16,
            'map_width': 800,
            'map_height': 500,}))
    class Meta:
        model = Segment
        fields = ('geom',)
        

class ChangeSegmentAttributesForm(forms.ModelForm):
    class Meta:
        model = Segment
        fields = ('width', 'cover_type')


class OperationSegmentForm(forms.ModelForm):

    class Meta:
        model = OperationSegment
        fields = ('date',)
