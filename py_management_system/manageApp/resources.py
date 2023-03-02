from .models import DepartmentModel,EmployeeTypeModel,EmployeeModel,SalaryModel,ProjectModel,SummaryModel,PmSummaryModel,InvoiceModel,ProjectDetailsModel
from import_export import resources
from import_export import resources,fields
from import_export.widgets import ForeignKeyWidget,ManyToManyWidget
import datetime

class DepartmentResource(resources.ModelResource):
    class Meta:
        model = DepartmentModel
        fields = ('id','department_name')
     
    def before_import_row(self, row, row_number=None, **kwargs):
                    
        if row.get('department_name') is None:
            print("Blank Department Data")
        else :
            department_name = row.get('department_name')
            print("Department NAME = ",department_name)
            new_department_name = department_name.capitalize()
            print("NEW Department NAME == ",new_department_name)
            row['department_name'] = new_department_name
            
        return super().before_import_row(row, row_number, **kwargs)
       
class EmployeeTypeResource(resources.ModelResource):
    class Meta:
        model = EmployeeTypeModel
        fields = ('id','employee_type')
    
        
    def before_import_row(self, row, row_number=None, **kwargs):
                    
        if row.get('employee_type') is None:
            print("Blank employee_type Data")
        else :
            employee_type = row.get('employee_type')
            new_employee_type = employee_type.capitalize()
            row['employee_type'] = new_employee_type
            
        return super().before_import_row(row, row_number, **kwargs)
     
class EmployeeResource(resources.ModelResource): 
    set_unique = set()
    department = fields.Field(attribute='department',widget=ForeignKeyWidget(DepartmentModel, 'department_name'),column_name='department')       
    employee_type = fields.Field(attribute='employee_type',widget=ForeignKeyWidget(EmployeeTypeModel, 'employee_type'),column_name='employee_type')       
    employee_status = fields.Field(attribute='status')
    class Meta:
        model = EmployeeModel
        fields = ('id','employee_name','employee_email','joining_date','relieving_date','department','employee_type','salary_ctc','employee_status','comments')
        export_order = ('employee_name','employee_email','joining_date','relieving_date','department','employee_type','salary_ctc','employee_status','comments')
        skip_unchanged = True
        skip_diff = False
   
    
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        self.set_unique = set()
        print('Row Data = ',dataset._Dataset__headers)
        if dataset._Dataset__headers:
            column_name = dataset._Dataset__headers
            # print("COLUMN NAME = ",column_name)
            low = list(map(lambda x: x.lower(), column_name))
            # print("LOWER == ",low)
            dataset._Dataset__headers = low
        
    def before_import_row(self, row, row_number=None, **kwargs):
        # Employee Name
        if row.get('employee_name') is None:
            print("Blank employee_name Data")
        else :
            employee_name = row.get('employee_name')
            new_employee_name = employee_name.title()
            row['employee_name'] = new_employee_name
            
        # Employee Email
        if row.get('employee_email') is None:
            print("Blank employee_email Data")
        else :
            employee_email = row.get('employee_email')
            new_employee_email = employee_email.lower()
            row['employee_email'] = new_employee_email
            
        # Joining Date   
        if row.get('joining_date') is None:
            print("Blank joining_date Data")
        else :
            joining_date = row.get('joining_date')
            con_date = datetime.datetime.strptime(joining_date, '%d-%m-%Y')
            new_date = datetime.datetime.strftime(con_date, '%Y-%m-%d')
            row['joining_date'] = new_date
        
        # Relieving Date 
        if row.get('relieving_date') is None:
            print("Blank relieving_date Data")
        else :
            relieving_date = row.get('relieving_date')
            rel_date = datetime.datetime.strptime(relieving_date, '%d-%m-%Y')
            new_relieving_date = datetime.datetime.strftime(rel_date, '%Y-%m-%d')
            row['relieving_date'] = new_relieving_date
        
        # Department Name
        if row.get('department') is None:
            print("Blank department Data")
        else :
            department = row.get('department')
            new_dept = department.title()
            print("NEW DEPARTMENT = ",new_dept)
            row['department'] = new_dept
        
        # Employee Type Name
        if row.get('employee_type') is None:
            print("Blank employee_type Data")
        else :
            employee_type = row.get('employee_type')
            new_employee_type = employee_type.title()
            row['employee_type'] = new_employee_type
        
        relieving_date = row.get('relieving_date')
        status = row.get('employee_status')
        print("Relieving Date = ",relieving_date," ","Status = ",status)
        if relieving_date:
            new_status = 'Relieve'
            row['employee_status'] = new_status
        # else:
            # new_status = 'Confirmed'
            # row['employee_status'] = new_status
            
        return super().before_import_row(row, row_number, **kwargs)
        
    def skip_row(self, instance, original, row, import_validation_errors=None):
        employee_qs = EmployeeModel.objects.filter(
            employee_name=instance.employee_name,
            employee_email=instance.employee_email,
            joining_date=instance.joining_date,
            relieving_date=instance.relieving_date,
        )
        employee_email = instance.employee_email
        
        if employee_email in self.set_unique:
            return True
        else:
            self.set_unique.add(employee_email)
            
        print("employee_qs = ",employee_qs)
        if instance.employee_name is None:
            return True
        else:
            print('Employee Name None')
            
        if employee_qs is None:
            return True
        
        if employee_qs.exists():
            return True
        else:
            print('Record All Ready Exists')
            
        return super().skip_row(instance, original, row, import_validation_errors)
       
class SalaryResources(resources.ModelResource):
    employee_email = fields.Field(attribute='employee',widget=ForeignKeyWidget(EmployeeModel, 'employee_email'))
    Salary = fields.Field(attribute='salary',column_name='Salary')
    class Meta:
        model =  SalaryModel
        fields = ('id','month','year','salary','employee_email','payment_mode','per_hrs_cost_inr','per_hrs_cost_dollar','comments')
        export_order = ('month','year','salary','employee_email','payment_mode','per_hrs_cost_inr','per_hrs_cost_dollar','comments')
        import_order = fields
        skip_unchanged = True
        skip_diff = False
    
    def before_import_row(self, row, row_number=None, **kwargs):
        if row.get('month') is not None:
            month = row.get('month')
            new_month = month.title()
            row['month'] = new_month
        
    def skip_row(self, instance, original, row, import_validation_errors=None):
        salary_qs = SalaryModel.objects.filter(
            month=instance.month,
            year=instance.year,
            salary=instance.salary,
        )
        
        if instance.month is None:
            return True
        else:
            print('Month None')
            
        if salary_qs is None:
            return True
        
        return super().skip_row(instance, original, row, import_validation_errors)
    
    
class ProjectResources(resources.ModelResource):
    set_unique = set()
    bde = fields.Field(attribute='bde_name',widget=ForeignKeyWidget(EmployeeModel, 'employee_email'))
    project_manager = fields.Field(attribute='project_manager',widget=ForeignKeyWidget(EmployeeModel, 'employee_email'))
    dt_created_at = fields.Field(attribute='project_start_date')
    dt_modified_at = fields.Field(attribute='project_end_date')
    
    class Meta:
        model = ProjectModel
        fields = ('id','project_title','project_customer','bde','mode','expected_hrs','status','project_manager','dt_created_at','dt_modified_at','comments')
        export_order = ('project_title','project_customer','bde','mode','expected_hrs','status','project_manager','dt_created_at','dt_modified_at','comments')
        skip_unchanged = True
        skip_diff = False
        
    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
    #     print('Row Data = ',dataset._Dataset__headers)
    #     if dataset._Dataset__headers:
    #         column_name = dataset._Dataset__headers
    #         print("COLUMN NAME = ",column_name)
    #         low = list(map(lambda x: x.lower(), column_name))
    #         print("LOWER == ",low)
    #         dataset._Dataset__headers = low
            
    def before_import_row(self, row, row_number=None, **kwargs):
        # Project start Date
        if row.get('dt_created_at') is not None:
            project_start_date = row.get('dt_created_at')
            print("Project Start Date = ",project_start_date,type(project_start_date))
            datetime_object = datetime.datetime.strptime(project_start_date, '%Y-%m-%d %H:%M:%S')
            print("Datetime Object = ",datetime_object)
            new_start_date = datetime_object.strftime("%Y-%m-%d")
            print("New = ",new_start_date)
            row['dt_created_at'] = new_start_date
            
        #  Project End Date 
        if row.get('dt_modified_at') is not None:
            project_end_date = row.get('dt_modified_at')            
            datetime_object = datetime.datetime.strptime(project_end_date, '%Y-%m-%d %H:%M:%S')
            new_end_date = datetime_object.strftime("%Y-%m-%d")
            row['dt_modified_at'] = new_end_date
        
        #  Status
        if row.get('status') is not None:
            status = row.get('status')
            new_status = status.title()
            if new_status == 'Active':
                row['status'] = 1
            if new_status == 'Inactive':
                row['status'] = 2
        
        # Mode 
        if row.get('mode') is not None:
            mode = row.get('mode')
            new_mode = mode.title()
            if new_mode == 'Fixed':
                row['mode'] = 1
            if new_mode == 'Hourly':
                row['mode'] = 2   
            if new_mode == 'Monthly':
                row['mode'] = 3 
        
        # Expected Hours
        # if row.get('expected_hrs') is None or 0:
        #     row.get['expected_hrs'] = '00:00'
        # else:
        #     expected_hrs = row.get('expected_hrs')
        #     print("Expected Hours = ",expected_hrs,type(expected_hrs))
        #     row.get['expected_hrs'] = expected_hrs
        
    def skip_row(self, instance, original, row, import_validation_errors=None):
        project_qs = ProjectModel.objects.filter(
            project_title=instance.project_title,
            project_customer=instance.project_customer,
            mode=instance.mode,
            expected_hrs=instance.expected_hrs,
            status=instance.status,
            project_start_date=instance.project_start_date,
            project_end_date=instance.project_end_date,
        )
        project_title = instance.project_title
        
        if project_title in self.set_unique:
            return True
        else:
            self.set_unique.add(project_title)
            
        print("project_qs = ",project_qs)
        if instance.project_title is None:
            return True
            
        if project_qs is None:
            return True
        
        if project_qs.exists():
            return True
        else:
            print('Record All Ready Exists')
            
        return super().skip_row(instance, original, row, import_validation_errors)

class InvoiceResources(resources.ModelResource):
    class Meta:
        model = InvoiceModel
        fields = ('id','month','year','project_name','invoice_amount','per_hrs_rate_inr','per_hrs_rate_dollar')
        export_order = ('month','year','project_name','invoice_amount','per_hrs_rate_inr','per_hrs_rate_dollar')
        skip_unchanged = True
        skip_diff = False
        
class PmSummaryResource(resources.ModelResource):
    pm_name = fields.Field(attribute='pm_name',widget=ForeignKeyWidget(EmployeeModel, 'employee_email'))
    project = fields.Field(attribute='project',widget=ForeignKeyWidget(ProjectModel, 'project_name'))
    
    class Meta:
        model = PmSummaryModel
        fields = ('id','pm_name','month','year','total_freeze_hrs','total_billable_hrs','existing_client_hrs','new_client_hrs','total_active_developer','no_of_resources')        
        export_order = ('pm_name','month','year','total_freeze_hrs','total_billable_hrs','existing_client_hrs','new_client_hrs','total_active_developer','no_of_resources')  
        import_order = fields
        skip_unchanged = True
        skip_diff = False
            
    def skip_row(self, instance, original, row, import_validation_errors=None):
        project_data_qs = PmSummaryModel.objects.filter(
            month = instance.month,
            year = instance.year,
            total_freeze_hrs = instance.total_freeze_hrs,
            total_billable_hrs = instance.total_billable_hrs,
            no_of_resources = instance.no_of_resources,
        )
        print("project_qs = ",project_data_qs)
        if instance.month is None:
            return True
        else:
            print('Month None False')
            
            
        if project_data_qs is None:
            return True
        
        if project_data_qs.exists():
            return True
        else:
            print('False')
        return super().skip_row(instance, original, row, import_validation_errors)
    
class SummaryResource(resources.ModelResource):    
    class Meta:
        model = SummaryModel
        fields = ('id','month','year','total_headcount','technical_team','active_developer','total_working_day','total_expected_hrs','total_freeze_hrs','new_client_hrs','existing_client_hrs','total_billable_hrs','total_utilization','total_income','total_expense','profit','per_resource_cost')        
        export_order = ('month','year','total_headcount','technical_team','active_developer','total_working_day','total_expected_hrs','total_freeze_hrs','new_client_hrs','existing_client_hrs','total_billable_hrs','total_utilization','total_income','total_expense','profit','per_resource_cost')  
        import_order = fields
        skip_unchanged = True
        skip_diff = False    

class ProjectDetailsResource(resources.ModelResource):    
    class Meta:
        model = ProjectDetailsModel
        fields = ('id','month','year','project_name','project_manager','resource_name','billable_hrs','spent_hrs','per_hrs_cost_inr','per_hrs_cost_dollar','per_hrs_rate_inr','per_hrs_rate_dollar','total_cost_inr','total_rate_inr','total_cost_dollar','total_rate_dollar','profit')        
        export_order = ('month','year','project_name','project_manager','resource_name','billable_hrs','spent_hrs','per_hrs_cost_inr','per_hrs_cost_dollar','per_hrs_rate_inr','per_hrs_rate_dollar','total_cost_inr','total_rate_inr','total_cost_dollar','total_rate_dollar','profit')  
        import_order = fields
        skip_unchanged = True
        skip_diff = False      