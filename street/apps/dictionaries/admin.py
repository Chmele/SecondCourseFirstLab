from django.contrib import admin
from django.db import models
from .models import *

admin.site.register(DictStreetOperations)
admin.site.register(DictStreetGeomType)
admin.site.register(DictStreetTopocode)
admin.site.register(DictStreetTract)
admin.site.register(DictStreetType)
admin.site.register(DictDistricts)
admin.site.register(DictBalanceHolder)


admin.site.site_header = "Служба дизлокації ТЗРДР"
admin.site.site_title = "Адмін-сторінка зміни складу вуличних об'єктів"
admin.site.index_title = "Адмін-сторінка зміни складу вуличних об'єктів"
