from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
 

class DepartmentModel(models.Model):
    department_name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "department_master"
        verbose_name = 'Department Model'
        
    def __str__(self):
        return self.department_name 
    
    def save(self, force_insert=False, force_update=False):
        self.department_name = self.department_name.title()
        super(DepartmentModel, self).save(force_insert, force_update)
          
class EmployeeTypeModel(models.Model):
    employee_type = models.CharField(max_length=100)
    
    class Meta:
        db_table = "employee_type_master"  
        verbose_name = 'EmployeeType Model'
        
    def __str__(self):
        return self.employee_type 

    def save(self, force_insert=False, force_update=False):
        self.employee_type = self.employee_type.title()
        super(EmployeeTypeModel, self).save(force_insert, force_update)
        
class EmployeeModel(models.Model):
    STATUS_CHOICE = [
        ("1", "Probation"),
        ("2", "Confirmed"),
        ("3", "Notice"),
        ("4", "Terminate"),
        ("5", "Relieve"),
    ]
    employee_name = models.CharField(max_length=255)
    employee_email = models.EmailField(max_length=100,unique=False)
    joining_date = models.DateField(null=True)
    relieving_date = models.DateField(blank=True,null=True)
    department = models.ForeignKey(DepartmentModel,on_delete=models.CASCADE)
    employee_type = models.ForeignKey(EmployeeTypeModel,on_delete=models.CASCADE)
    salary_ctc = models.CharField(max_length=100,default='0',blank=True)
    status = models.CharField(max_length=100,choices=STATUS_CHOICE,default='',blank=True)
    comments = models.CharField(max_length=100,default="",null=True,blank=True)
    joining_month = models.CharField(max_length=100,default='',null=True,blank=True)
    joining_year = models.CharField(max_length=100,default="",null=True,blank=True)
    relieving_month = models.CharField(max_length=100,default="",null=True,blank=True)
    relieving_year = models.CharField(max_length=100,default="",null=True,blank=True)
    class Meta:
        db_table = "employee_master"
        unique_together = ('employee_email',)
        verbose_name = 'Employee Model'
        
    def __str__(self):
        return self.employee_name 
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.employee_name = self.employee_name.title()
        self.employee_email = self.employee_email.lower()
        
        if self.joining_date is None:
            print("Blank joining_date Data")
        else:
            self.joining_date = self.joining_date
            self.joining_month = self.joining_date.strftime("%b")
            self.joining_year = self.joining_date.strftime("%Y")
            print("joining_month = ",self.joining_month)
            print("joining_year = ",self.joining_year)
        
        if self.relieving_date is None:
            print("Blank Relieving_date")
        else:
            self.relieving_date = self.relieving_date
            self.relieving_month = self.relieving_date.strftime("%b")
            self.relieving_year = self.relieving_date.strftime("%Y")
            print("relieving_month = ",self.relieving_month)
            print("relieving_year = ",self.relieving_year)
        super(EmployeeModel, self).save(force_insert, force_update,*args, **kwargs)
          
class SalaryModel(models.Model):
    PAYMENT_CHOICE = [
        ("1", "Online"),
        ("2", "Default"),
        ("3", "F&F"),
    ]
    def current_year():
        return datetime.date.today().year
    
    def max_value_current_year(value):
        return MaxValueValidator(datetime.date.today().year)(value)

    month = models.CharField(max_length=100,default=None)
    year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    salary = models.FloatField(default=None,null=True)
    employee = models.ForeignKey(EmployeeModel,on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=100,choices=PAYMENT_CHOICE,default='2',blank=True)
    per_hrs_cost_inr = models.FloatField(default='0',blank=True,null=True)
    per_hrs_cost_dollar = models.DecimalField(max_digits=5, decimal_places=2,default='0',blank=True,null=True)
    comments = models.CharField(max_length=100,default="",null=True,blank=True)
    
    class Meta:
        db_table = "salary_master"
        verbose_name = 'Salary Model'
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.month = self.month.title()        
        super(SalaryModel, self).save(force_insert, force_update,*args, **kwargs)
        
class ProjectModel(models.Model):
    MODE_CHOICE = [
        ("1", "Fixed"),
        ("2", "Hourly"),
        ("3", "Monthly"),
    ]
    
    STATUS_CHOICE = [
        ("1", "Active"),
        ("2", "Inactive"),
    ]
    project_title = models.CharField(max_length=100,default='',unique=True)
    project_customer = models.CharField(max_length=255,default='')
    bde_name = models.ForeignKey(EmployeeModel,on_delete=models.CASCADE)#BDE_ID
    mode = models.CharField(max_length=100,choices=MODE_CHOICE,default='',blank=True)
    expected_hrs = models.CharField(max_length=255,default='00:00',blank=True)
    status = models.CharField(max_length=100,choices=STATUS_CHOICE,default='1',blank=True)
    project_manager = models.ForeignKey(EmployeeModel,on_delete=models.CASCADE,related_name='project_manager',default='')#PM_ID
    project_start_date = models.DateField(default='',null=True)
    project_end_date = models.DateField(default='',null=True)
    comments = models.CharField(max_length=100,default="",null=True,blank=True)
    
    class Meta:
        db_table = "project_master"
        verbose_name = 'Project Model'
         
    def __str__(self):
        return self.project_title 
    
    def save(self, force_insert=False, force_update=False):
        # self.project_title = self.project_title.title()
        self.project_customer = self.project_customer.title()
        print("PROJECT NAME = ",self.project_title)
        super(ProjectModel, self).save(force_insert, force_update)
        
class PmSummaryModel(models.Model):
    def current_year():
        return datetime.date.today().year
    
    def max_value_current_year(value):
        return MaxValueValidator(datetime.date.today().year)(value)

    pm_name = models.ForeignKey(EmployeeModel,on_delete=models.CASCADE)#PM_ID
    month = models.CharField(max_length=100)
    year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    total_freeze_hrs = models.CharField(max_length=255)
    total_billable_hrs = models.CharField(max_length=255)
    existing_client_hrs = models.CharField(max_length=255,default='')
    new_client_hrs = models.CharField(max_length=255,default='')
    no_of_resources = models.IntegerField()
    total_active_developer = models.IntegerField(default=0)
    pm_flag = models.BooleanField(default=False)
    submit_flag = models.BooleanField(default=False)
    
    class Meta:
        db_table = "pm_summary_master"
        verbose_name = 'PMSummary Model'
       
class SummaryModel(models.Model):
    month = models.CharField(max_length=255,default='')
    year = models.IntegerField(default=0)
    total_headcount = models.IntegerField(default=0)
    technical_team = models.IntegerField(default=0)
    active_developer = models.IntegerField(default=0)
    total_working_day = models.IntegerField(default=0)
    total_expected_hrs = models.CharField(max_length=255,default='00:00')
    total_freeze_hrs = models.CharField(max_length=255,default='00:00')
    new_client_hrs = models.CharField(max_length=255,default='00:00')
    existing_client_hrs = models.CharField(max_length=255,default='00:00')
    total_billable_hrs = models.CharField(max_length=255,default='00:00')
    total_utilization = models.FloatField(default=0)
    total_income = models.IntegerField(default=0)
    total_expense = models.IntegerField(default=0)
    profit = models.FloatField(default=0)
    per_resource_cost = models.FloatField(default=0)
    flag = models.BooleanField(default=False)
    
    class Meta:
        db_table = "summary_master"
        verbose_name = 'Summary Model' 

#Invoice Model
class InvoiceModel(models.Model):
    def current_year():
        return datetime.date.today().year
    
    def max_value_current_year(value):
        return MaxValueValidator(datetime.date.today().year)(value)
    
    month = models.CharField(max_length=100,default=None)
    year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    project_name = models.ForeignKey(ProjectModel,on_delete=models.CASCADE)
    invoice_amount = models.FloatField()
    per_hrs_rate_inr = models.FloatField(default='0')
    per_hrs_rate_dollar = models.FloatField(default='0')
    
    class Meta:
        db_table = 'invoice_master'
        verbose_name = 'Invoice Model'
    

class ProjectDetailsModel(models.Model):
    month = models.CharField(max_length=255)
    year = models.IntegerField(default=0)
    project_name = models.ForeignKey(ProjectModel,on_delete=models.CASCADE)
    project_manager = models.ForeignKey(EmployeeModel,on_delete=models.CASCADE)
    resource_name = models.ForeignKey(EmployeeModel,on_delete=models.CASCADE,related_name='resource_name')
    billable_hrs = models.CharField(max_length=255,default='00:00')
    spent_hrs = models.CharField(max_length=255,default='00:00')
    per_hrs_cost_inr = models.FloatField(default='0.0')
    per_hrs_cost_dollar = models.FloatField(default='0.0')
    per_hrs_rate_inr = models.FloatField(default='0.0')
    per_hrs_rate_dollar = models.FloatField(default='0.0')
    total_cost_inr = models.FloatField(default='0.0')
    total_rate_inr = models.FloatField(default='0.0')
    total_cost_dollar = models.FloatField(default='0.0')
    total_rate_dollar = models.FloatField(default='0.0')
    profit = models.FloatField(default='0.0')
    
    class Meta:
        db_table = 'project_details_master'
        verbose_name = "Project Details Model"