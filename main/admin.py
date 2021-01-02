from django.contrib import admin
from main.models import Schemas, SchemasColumn, DataSets


# Register your models here.

admin.site.register(Schemas)
admin.site.register(SchemasColumn)
admin.site.register(DataSets)

