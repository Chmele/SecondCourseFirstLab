from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.search, name='search'),
    path('stats/', views.StatsView, name = 'stats'),
    path('<int:street_id>/segment/<int:segment_id>/', views.segment_detail, name='segment_detail'),
    path('street_chronology/<int:street>', views.StreetChronologyView, name = 'street_chronology' ),
    path('search_ajax/', views.search_ajax, name = 'search_ajax'),
    path('<int:street_id>/', views.detail, name='detail'),
    path('document/new/', views.document_new, name='document_new'),
    path('street/new/', views.street_new, name='street_new'),
    path('<int:street_id>/street/rename/', views.street_rename, name='street_rename'),
    path('<int:street_id>/segment/new/', views.segment_new, name='segment_new'),
    path('operations/<int:doc_id>/', views.operations, name='operations'),
    path('<int:street_id>/segment/<int:segment_id>/change/geom/', views.segment_change_geom, name='segment_change_geom'),
    path('<int:street_id>/segment/<int:segment_id>/change/attributes/', views.segment_change_attributes, name='segment_change_attributes'),
]
