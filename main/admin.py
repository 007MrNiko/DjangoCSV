from django.contrib import admin
from main.models import Schemas, SchemasColumn, DataSets


# Custom admin panel interfaces
@admin.register(Schemas)
class SchemasAdmin(admin.ModelAdmin):
    def schema_owner(self, obj):
        return obj.user.username

    list_display = ("name", "schema_owner", "last_modified")
    search_fields = ("name",)


@admin.register(SchemasColumn)
class SchemasColumnAdmin(admin.ModelAdmin):
    def schema_owner(self, obj):
        return obj.schema.user.username

    def schema_name(self, obj):
        return obj.schema.name

    list_display = ("name", "schema_name", "category", "schema_owner", "order")
    search_fields = ("name", "category")


@admin.register(DataSets)
class DataSetsAdmin(admin.ModelAdmin):
    def schema_owner(self, obj):
        return obj.schema.user.username

    def schema_name(self, obj):
        return obj.schema.name

    list_display = ("date_created", "schema_name", "schema_owner", "rows", "ready")
    search_fields = ("ready", "date_created")

