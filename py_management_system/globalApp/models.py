from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class MonthDataModel(models.Model):
    def current_year():
        return datetime.date.today().year
    
    def max_value_current_year(value):
        return MaxValueValidator(datetime.date.today().year)(value)
    
    month = models.CharField(max_length=100,default=None)
    year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    dollar_rate = models.FloatField()
    total_expense =  models.IntegerField(default=0)
    per_table_cost = models.FloatField()
    working_day = models.IntegerField()
    per_hrs_fix_cost = models.FloatField()
        
    class Meta:
        db_table = 'month_global_data_master'
        verbose_name = 'MonthlyData Model'