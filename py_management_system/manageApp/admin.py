from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import DepartmentModel,EmployeeTypeModel,EmployeeModel,SalaryModel,ProjectModel,SummaryModel,PmSummaryModel,InvoiceModel,ProjectDetailsModel
from .resources import DepartmentResource,EmployeeTypeResource,EmployeeResource,SalaryResources,ProjectResources,SummaryResource,PmSummaryResource,InvoiceResources
from rangefilter.filters import DateRangeFilter
from django.db.models import Q
import datetime
# Register your models here.
@admin.register(DepartmentModel)
class DepartmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DepartmentResource
    list_display = ['department_name']
    
    class Meta:
        model = DepartmentModel
   
@admin.register(EmployeeTypeModel)
class EmployeeTypeAdminModel(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = EmployeeTypeResource
    list_display = ['employee_type']
    
    class Meta:
        model = EmployeeTypeModel

@admin.register(EmployeeModel)
class EmployeeAdminModel(ImportExportModelAdmin, admin.ModelAdmin):
    
    def custom_titled_filter(title):
        class Wrapper(admin.FieldListFilter):
            def __new__(cls, *args, **kwargs):
                instance = admin.FieldListFilter.create(*args, **kwargs)
                instance.title = title
                return instance
        return Wrapper

  
    save_as = True 
    resource_class = EmployeeResource
    list_display = ['employee_name','employee_email','joining_date','relieving_date','department_','employee_type_','salary_ctc','status_','comments','relieving_month','relieving_year']
    list_filter = [('joining_date',DateRangeFilter),('relieving_date',DateRangeFilter),(('joining_date',custom_titled_filter('Duration of Joining Date'))),(('relieving_date',custom_titled_filter('Duration of Relieving Date'))),('department__department_name',custom_titled_filter('Department')),('employee_type__employee_type',custom_titled_filter('Employee_Type')),('status',custom_titled_filter('Employee Status'))]
    search_fields = ('employee_name', )
    def department_(self,obj):
        return obj.department.department_name
    
    def employee_type_(self,obj):
        return obj.employee_type.employee_type
    
    def status_(self,obj):
        return obj.status
    
    def joining_month(self, obj):
        j_date = obj.joining_date
        join_month = j_date.strftime("%b")
        return join_month
    
    def joining_year(self,obj):
        j_year = obj.joining_date
        join_year = j_year.strftime("%Y")
        return join_year
    
    def relieving_month(self, obj):
        r_date = obj.relieving_date
        if r_date is None:
            print(r_date)
        else:
            print(type(r_date),r_date.strftime("%b"))
            relieve_month = r_date.strftime("%b")
            return relieve_month
    
    def relieving_year(self,obj):
        r_year = obj.relieving_date
        if r_year is None:
            print(r_year)
        else:
            relieve_year = r_year.strftime("%Y")
            return relieve_year
        
    class Meta:
        model = EmployeeModel

@admin.register(SalaryModel)
class SalaryAdminModel(ImportExportModelAdmin, admin.ModelAdmin):
    
    def custom_titled_filter(title):
        class Wrapper(admin.FieldListFilter):
            def __new__(cls, *args, **kwargs):
                instance = admin.FieldListFilter.create(*args, **kwargs)
                instance.title = title
                return instance
        return Wrapper
    
    resource_class = SalaryResources
    list_display = ['month','year','salary','employee','payment_mode','per_hrs_cost_inr','per_hrs_cost_dollar','comments']
    list_filter = [(('month',custom_titled_filter('Month'))),(('year',custom_titled_filter('Year'))),(('employee',custom_titled_filter('Employee')))]
    search_fields = ('employee__employee_name', )
    
    # def related_employee_(self, obj):
    #     return obj.employee.employee_name
    # related_employee_.short_description = 'Employee'
    
    class Meta:
        model = SalaryModel

class BDEFilter(admin.SimpleListFilter):
    title = 'BDE'
    parameter_name = 'BDE'
    def lookups(self, request, model_admin):
        bde = [(one_pm.id, one_pm.employee_name) for one_pm in EmployeeModel.objects.filter(employee_type__employee_type='Bde')]
        # print("BDE = ",bde)
        return bde

    def queryset(self, request, queryset):
        id_of_bde = EmployeeModel.objects.filter(id=self.value()).first()
        # print("ID OF BDE = ",id_of_bde)
        if id_of_bde:
            return queryset.filter(bde_name__employee_name=id_of_bde.employee_name)  
        
class PMFilter(admin.SimpleListFilter):
    title = 'Project Manager'  # or use _('country') for translated title
    parameter_name = 'Project Manager'
    def lookups(self, request, model_admin):
        pm = [(one_pm.id, one_pm.employee_name) for one_pm in EmployeeModel.objects.filter(employee_type__employee_type='Pm')]
        # print("PM = ",pm)
        return pm

    def queryset(self, request, queryset):
        id_of_pm = EmployeeModel.objects.filter(id=self.value()).first()
        # print("ID OF PM = ",id_of_pm)
        if id_of_pm:
            return queryset.filter(pm_name__employee_name=id_of_pm.employee_name) 
@admin.register(ProjectModel)
class ProjectAdminModel(ImportExportModelAdmin, admin.ModelAdmin):
    def custom_titled_filter(title):
        class Wrapper(admin.FieldListFilter):
            def __new__(cls, *args, **kwargs):
                instance = admin.FieldListFilter.create(*args, **kwargs)
                instance.title = title
                return instance
        return Wrapper
    
    resource_class = ProjectResources
    list_display = ['project_title','project_customer','bde_name','mode','expected_hrs','status','project_manager','project_start_date','project_end_date','comments']
    list_filter = [BDEFilter,PMFilter,(('status',custom_titled_filter('Project Status'))),(('project_title',custom_titled_filter('Project Title')))]
    search_fields = ('project_title','bde_name__employee_name','project_manager__employee_name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project_manager":
            kwargs["queryset"] = EmployeeModel.objects.filter(employee_type__employee_type='Pm')
        if db_field.name == "bde_name":
            kwargs["queryset"] = EmployeeModel.objects.filter(employee_type__employee_type='Bde')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
        
    # def project_start_date_(self,obj):
    #     p_date = obj.project_start_date
    #     datetime_object = datetime.datetime.strptime(p_date, '%Y-%m-%d %H:%M:%S')
    #     new_datetime_object = datetime.datetime.strptime(datetime_object, '%Y-%m-%d %H:%M:%S')
    #     project_start_date = datetime.datetime.strftime(new_datetime_object,"%b %d %Y")
    #     return project_start_date
    
    # def project_end_date_(self,obj):
    #     p_date = obj.project_end_date
    #     # print("Project _date = ",p_date,type(p_date))
    #     datetime_object = datetime.datetime.strftime(p_date, '%Y-%m-%d %H:%M:%S')
    #     # print("datetime Object = ",datetime_object,type(datetime_object))
    #     new_datetime_object = datetime.datetime.strptime(datetime_object, '%Y-%m-%d %H:%M:%S')
    #     # print("New Datetime Object = ",new_datetime_object)
    #     project_end_date = datetime.datetime.strftime(new_datetime_object,"%b %d %Y")
    #     # print("Project Date = ",project_end_date)
    #     return project_end_date
    class Meta:
        model = ProjectModel
@admin.register(PmSummaryModel)
class PmSummaryAdminModel(ImportExportModelAdmin, admin.ModelAdmin):
    
    def custom_titled_filter(title):
        class Wrapper(admin.FieldListFilter):
            def __new__(cls, *args, **kwargs):
                instance = admin.FieldListFilter.create(*args, **kwargs)
                instance.title = title
                return instance
        return Wrapper
    
    
    resource_class = PmSummaryResource
    list_display = ['month','year','pm_name','total_freeze_hrs','new_client_hrs','existing_client_hrs','total_billable_hrs','no_of_resources','total_active_developer',]
    list_filter = [(('month',custom_titled_filter('Month'))),(('year',custom_titled_filter('Year'))),PMFilter]
    # def related_project_(self, obj):
    #     return obj.project.project_name
    # related_project_.short_description = 'Project Name'

    def get_queryset(self, request):
        respective_data = super(PmSummaryAdminModel, self).get_queryset(request)
        emp_type_obj = EmployeeTypeModel.objects.get(employee_type = 'Pm')
        print("-----emp_type_obj---", emp_type_obj)        
        return respective_data.filter(pm_name__employee_type__employee_type='Pm')
    
    class Meta:
        model = PmSummaryModel
        
@admin.register(SummaryModel)
class SummaryDataAdminModel(ImportExportModelAdmin):
    def custom_titled_filter(title):
            class Wrapper(admin.FieldListFilter):
                def __new__(cls, *args, **kwargs):
                    instance = admin.FieldListFilter.create(*args, **kwargs)
                    instance.title = title
                    return instance
            return Wrapper
        
    resource_class = SummaryResource
    list_display = ['month','year','total_headcount','technical_team','active_developer','total_working_day','total_expected_hrs','total_freeze_hrs','new_client_hrs','existing_client_hrs','total_billable_hrs','total_utilization','total_income','total_expense','profit','per_resource_cost']
    list_filter = [(('month',custom_titled_filter('Month'))),(('year',custom_titled_filter('Year')))]
    
#Invoice Model
@admin.register(InvoiceModel)
class InvoiceAdminModel(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = InvoiceResources
    list_display = ['month','year','project_name','invoice_amount','per_hrs_rate_inr','per_hrs_rate_dollar']
    
@admin.register(ProjectDetailsModel)
class ProjectDetailsAdminModel(ImportExportModelAdmin , admin.ModelAdmin):
    def custom_titled_filter(title):
            class Wrapper(admin.FieldListFilter):
                def __new__(cls, *args, **kwargs):
                    instance = admin.FieldListFilter.create(*args, **kwargs)
                    instance.title = title
                    return instance
            return Wrapper
        
    resource_class = SummaryResource
    list_display = ['month','year','project_name','project_manager','resource_name','billable_hrs','spent_hrs','per_hrs_cost_inr','per_hrs_cost_dollar','per_hrs_rate_inr','per_hrs_rate_dollar','total_cost_inr','total_rate_inr','total_cost_dollar','total_rate_dollar','profit']
    list_filter = [(('month',custom_titled_filter('Month'))),(('year',custom_titled_filter('Year')))]
       