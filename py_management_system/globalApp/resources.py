from .models import MonthDataModel
from import_export import resources
from import_export import resources,fields
from import_export.widgets import ForeignKeyWidget,ManyToManyWidget
import datetime

class MonthDataResource(resources.ModelResource):
    class Meta:
        model = MonthDataModel
        fields = ('id','month','year','dollar_rate','total_expense','per_table_cost','working_day','per_hrs_fix_cost')

       