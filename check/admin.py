from django.contrib import admin
from .models import TableSets,RulesForMono

# Register your models here.


@admin.register(TableSets)
class TableSets(admin.ModelAdmin):
    list_display = ('Tid', 'database_name', 'table_name', 'instance_name', 'create_time', 'last_modify_time')
    ordering = ('Tid',)

@admin.register(RulesForMono)
class TableSets(admin.ModelAdmin):
    list_display = ('rule_type', 'related_tables', 'create_time', 'last_modify_time')
    ordering = ('create_time',)
