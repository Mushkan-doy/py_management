from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from globalApp.models import MonthDataModel
from globalApp.resources import MonthDataResource
# Register your models here.

@admin.register(MonthDataModel)
class DepartmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MonthDataResource
    list_display = ['month','year','dollar_rate','total_expense','per_table_cost','working_day','per_hrs_fix_cost']
    
    class Meta:
        model = MonthDataModel
   