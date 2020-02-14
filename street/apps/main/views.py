import os
import copy

from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.http import Http404
from datetime import datetime, date
from django.db.models import Q, Count, Sum
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import DetailView, ListView
from qsstats import QuerySetStats
from dictionaries.models import *
from django.contrib.gis.db.models.functions import Length

def StatsView(request):
    streets = Street.objects.all()
    s = Segment.objects.all().distinct('district', 'street')
    values = [[i.name, s.filter(district=i.id).count()] for i in DictDistricts.objects.all()]


    split_by=25
    min_len=0
    max_len=5000
    step = (max_len - min_len) / split_by
    q = Segment.objects.values('street').annotate(leng = Sum(Length('geom')))
    ret = [[
        # "[ "
        # + str(int(min_len + step * i))
        # +", "
        # + str(int(min_len + step * (i + 1)))
        # + " )", 
        "≤ " + str(int(min_len + step * (i + 1))),
        q.filter(leng__gte= min_len + step * i)
         .filter(leng__lt= min_len + step * (i + 1))
         .count()]
        for i in range(split_by)]
    street_count = Street.objects.count()
    segment_count = Segment.objects.count()
    return render(request, 'main/stats.html', {'values':values, 'len_stat':ret, 'street_count': street_count, 'segment_count': segment_count,})


def CityDetailView(request):
    if request.method == 'POST' and 'date' in request.POST:
        dat = request.POST['date']
    else:
        dat = date.today()
    date_now = date.today()
    street_list = actual_streets(dat)
    segment_list = actual_segments(dat)[:1000]
    geom = [g.geom for g in segment_list]
    for i in range(len(geom)):
        if i == 0:
            sum = geom[i]
        else:
            sum += geom[i]
    street_count = street_list.count()
    return render(request, 'main/city-detail.html', {'geom':sum,'segment_list':segment_list,'street_list': street_list, 'street_count': street_count, 'date_now': str(date_now)})


def StreetChronologyView(request, street):
    if request.method == 'POST' and 'date' in request.POST:
        dat = request.POST['date']
        dat = datetime.strptime(dat, '%Y-%m-%d')
    else:
        dat = date.today()
    hash_street = AllChronologicSegments(street,dat)
    return render(request, 'main/street_chronology.html', {'street_id': street, 'date': dat, 'hash_street': hash_street})


def AllChronologicSegments(street, date):
    list = []
    list+=BeforeStreets(street)
    list.append(street)
    list+=LaterStreets(street)
    return SegmentListByDateAndStreets(list,date)


def LaterStreets(street):
    q = OperationStreet.objects.filter(old=street)
    list = []
    for i in q:
        if not i.new is None :
            list.append(i.new.id )
    plus_list=[]
    for i in list:
        plus_list+=LaterStreets(i)
    return list+plus_list


def BeforeStreets(street):
    q = OperationStreet.objects.filter(new=street)
    list = []
    for i in q:
        if not i.old is None :
            list.append(i.old.id )
    plus_list=[]
    for i in list:
        plus_list+=BeforeStreets(i)
    return list+plus_list


def SegmentListByDateAndStreets(streets,date):
    hash_street = {}
    for street_id in streets:
        street = Street.objects.get(id=street_id)
        segments = Segment.objects.filter(
            Q(street__id = street.id),
            Q(segmentstreet__date_start__lte = date)|Q(segmentstreet__date_start=None),
            Q(segmentstreet__date_end__gt = date)|Q(segmentstreet__date_end=None),
        )
        hash_street[street] = segments
    return hash_street


def search(request):
    if request.method == 'POST' and 'date' in request.POST:
        dat = request.POST['date']
    else:
        dat = date.today()
    date_now = date.today()
    street_list = actual_streets(dat)
    street_count = street_list.count()
    district_list = DictDistricts.objects.all()
    street_type_list = DictStreetType.objects.all()
    return render(request, 'main/street_list.html', {'street_list': street_list, 'street_count': street_count, 'district_list': district_list, 'street_type_list': street_type_list, 'date_now': str(date_now)})

def search_ajax(request):
    if request.is_ajax():
        searchDate = request.GET['searchDate']
        if not searchDate:
            searchDate = date.today()
        searchName = request.GET['searchName']
        street = actual_streets(searchDate)
        street = street.filter(Q(name__icontains=searchName) | Q(streetalternativename__name__icontains=searchName))

        district = int(request.GET['district'])
        type_street = int(request.GET['type'])

        if district > 0:
            street = street.filter(segmentstreet__segment__district = district)       

        if type_street > 0:
            street = street.filter(type__id = type_street)

        street = street.distinct().order_by('id')

        street_list = list(street.values_list('id', 'name', 'type__name'))
        count_of_segments = count_segments_for_streets(street_list, searchDate)
        response = {'street_list': street_list, 'count_of_segments': count_of_segments}

        return JsonResponse(response, safe=False)
    else:
        raise Http404

def segments_by_date(street, date):
    segment_list = Segment.objects.filter(
        Q(street__id=street.id),
        Q(segmentstreet__date_start__lte = date)|Q(segmentstreet__date_start=None),
        Q(segmentstreet__date_end__gt = date)|Q(segmentstreet__date_end=None),
    )
    return segment_list

def detail(request, street_id):
    street = Street.objects.get(id = street_id)

    if request.method == 'POST' and 'date' in request.POST:
        dat = request.POST['date']
        dat = datetime.strptime(dat, '%Y-%m-%d')
    else:
        dat = date.today()

    segment_list = segments_by_date(street, dat)

    x=[]
    y=[]
    sumx=0
    sumy=0
    xcoord = 30.5238
    ycoord = 50.45466
    for each in street.segments.all():
        x.append(each.geom.centroid.x)
        sumx+=each.geom.centroid.x
        y.append(each.geom.centroid.y)
        sumy+=each.geom.centroid.y
        if len(x):
            xcoord = sumx/len(x)
  
        if len(y):
            ycoord = sumy/len(y)
    
    return render(request, 'main/detail.html', {'street': street, 'segment_list': segment_list, 'xcoord': xcoord, 'ycoord': ycoord, 'segment_count': segment_list.count(), 'date_now': str(date.today())})


def segment_detail(request, street_id, segment_id):
    segment = Segment.objects.get(id = segment_id)
    xcoord = segment.geom.centroid.x
    ycoord = segment.geom.centroid.y
    return render(request, 'main/segment_detail.html', {'segment': segment, 'street_id': street_id, 'xcoord': xcoord, 'ycoord': ycoord})

def segment_change_geom(request, street_id, segment_id):
    if not 'doc_id' in request.session:
        return redirect('main:document_new')
    else:
        street = Street.objects.get(id = street_id)
        doc_id = request.session['doc_id']
        document = DocumentsStreet.objects.get(id = doc_id)
        segment = Segment.objects.get(id = segment_id)
        if request.method == "POST":
            form = SegmentChangeGeomForm(request.POST, instance=segment)
            if form.is_valid():
                segment_new = copy.copy(segment)
                segment_new.id = None

                segment_new.geom = form.save(commit=False).geom
                segment_new.save()

                form_operation = OperationSegmentForm(request.POST)
                operation = form_operation.save(commit=False)
                operation.document = document
                operation.new = segment_new
                operation.old = segment
                operation.save()

                street.segments.add(segment_new)

                segment_street = SegmentStreet.objects.get(street = street.id, segment = segment.id)
                segment_street.date_end = operation.date
                segment_street.save()

                segment_street = SegmentStreet.objects.get(street = street.id, segment = segment_new.id)
                segment_street.date_start = operation.date
                segment_street.save()

                return redirect('main:segment_detail', street_id=street.id, segment_id=segment_new.id)
        else:
            form = SegmentChangeGeomForm(instance=segment)
            form_operation = OperationSegmentForm()
            return render(request, 'main/segment_change_geom.html', {'form': form, 'form_operation': form_operation, 'document': document, 'segment': segment})


def segment_change_attributes(request, street_id, segment_id):
    pass


def document_new(request):
    if request.method == "POST":
        form = DocumentsStreetForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.save()
            path_to_file = "street/media/" + str(document.document)
            outdir = os.path.dirname(path_to_file)
            path_to_converted_file = os.path.splitext(str(document.document))[0] + ".pdf"
            os.system("libreoffice --headless --convert-to pdf " + path_to_file + " --outdir " + outdir)
            document.path_pdf = path_to_converted_file
            document.save()
            request.session['doc_id'] = document.id
            return redirect('main:operations', doc_id=document.id)
    else:
        form = DocumentsStreetForm()
    return render(request, 'main/add_document.html', {'form': form})


def street_new(request):
    if not 'doc_id' in request.session:
        return redirect('main:document_new')
    else:
        doc_id = request.session['doc_id']
        document = DocumentsStreet.objects.get(id = doc_id)
        if request.method == "POST":
            form = StreetForm(request.POST)
            street = form.save(commit=False)
            street.save()
            form_operation = OperationStreetForm(request.POST)
            operation = form_operation.save(commit=False)
            operation.document = document
            operation.new = street
            operation.save()
            return redirect('main:detail', street_id=street.id)
        else:
            form = StreetForm()
            form_operation = OperationStreetForm()
            return render(request, 'main/add_street.html', {'form': form, 'form_operation': form_operation, 'document': document})


def street_rename(request, street_id):
    street = Street.objects.get(id = street_id)
    if not 'doc_id' in request.session:
        return redirect('main:document_new')
    else:
        doc_id = request.session['doc_id']
        document = DocumentsStreet.objects.get(id = doc_id)
        if request.method == "POST":
            street_name = request.POST['street_name']
            operation_date = request.POST['operation_date']
            new_street_id = street_rename_func(street_id, street_name, doc_id, operation_date)
            return redirect('main:detail', street_id=new_street_id)
        else:
            return render(request, 'main/rename_street.html', {'street': street, 'document': document})


def segment_new(request, street_id):
    if not 'doc_id' in request.session:
        return redirect('main:document_new')
    else:
        doc_id = request.session['doc_id']
        document = DocumentsStreet.objects.get(id = doc_id)
        street = Street.objects.get(id = street_id)
        if request.method == "POST":
            form = SegmentForm(request.POST)
            if form.is_valid():
                segment = form.save(commit=False)
                segment.save()

                form_operation = OperationSegmentForm(request.POST)
                operation = form_operation.save(commit=False)
                operation.document = document
                operation.new = segment
                operation.save()

                street.segments.add(segment)

                segment_street = SegmentStreet.objects.get(street = street_id, segment = segment.id)
                segment_street.date_start = operation.date
                segment_street.save()

                return redirect('main:detail', street_id=street_id)
        else:
            form = SegmentForm()
            form_operation = OperationSegmentForm()
            return render(request, 'main/add_segment.html', {'form': form, 'form_operation': form_operation, 'document': document, 'street': street})




def operations(request, doc_id):
    request.session['doc_id'] = doc_id
    document = DocumentsStreet.objects.get(id = doc_id)
    document_origin_name = os.path.basename(str(document.document))
    return render(request, 'main/operations.html', {'document': document})




#Осторожно : Писал Германюк!!!
def free_segments(request):
    not_free_id = SegmentStreet.objects.values('segment').distinct()
    segment_list = Segment.objects.exclude(id__in=not_free_id)
    return render(request, 'main/detail.html', {'free_segments': segment_list})

def street_rename_func(street_id, street_name, doc_id, operation_date):
    document = DocumentsStreet.objects.get(id = doc_id)
    street = Street.objects.get(id = street_id)
    new_street = copy.copy(street)
    new_street.name = street_name
    segments = street.segments.all()
    new_street.id = None
    new_street.save()
    segment_list = list(segments)
    pairs = SegmentStreet.objects.filter(street=street.id).filter(segment__in = segment_list)
    for p in pairs:
        p.date_end = operation_date
        p.save()
    for s in segments:
        new_street.segments.add(s)
    new_street.save()
    pairs = SegmentStreet.objects.filter(street=new_street.id)
    for p in pairs:
        p.date_start = operation_date
        p.save()
    operation = OperationStreet(old = street, new = new_street, document = document, date = operation_date)
    operation.save()
    return new_street.id

def actual_streets(date):
    result_list = []
    pairs = SegmentStreet.objects.all()
    actual_pairs = pairs.filter(
        Q(date_start__lt = date)|Q(date_start=None),
        Q(date_end__gte = date)|Q(date_end=None),
    )
    streetsInPairs = pairs.values_list('street',flat = True).distinct()
    result_list += actual_pairs.values_list('street',flat = True).distinct()
    streets = Street.objects.values_list('id', flat = True).exclude(id__in=streetsInPairs)
    result_list += streets
    ret = Street.objects.filter(id__in=result_list)
    return ret

def actual_segments(date):
    result_list = []
    pairs = SegmentStreet.objects.all()
    actual_pairs = pairs.filter(
        Q(date_start__lt = date)|Q(date_start=None),
        Q(date_end__gte = date)|Q(date_end=None),
    )
    segmentsInPairs = pairs.values_list('segment',flat = True).distinct()
    result_list += actual_pairs.values_list('segment',flat = True).distinct()
    segments = Segment.objects.values_list('id', flat = True).exclude(id__in=segmentsInPairs)
    result_list += segments
    ret = Segment.objects.filter(id__in=result_list)
    return ret

def count_segments_for_streets(streets, date):
    pairs = Street.segments.through.objects.filter(Q(date_start__lt = date)|Q(date_start=None),Q(date_end__gte = date)|Q(date_end=None),)
    streets_id_list = [s[0] for s in streets]
    pairs = pairs.filter(street__in=streets_id_list)
    result = pairs.values("street").annotate(count=Count("street")).order_by("street")
    result = list(result.values_list('count', flat = True))
    return result
