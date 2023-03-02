from django.shortcuts import render,redirect
from .models import EmployeeTypeModel,DepartmentModel,EmployeeModel,ProjectModel,SummaryModel,PmSummaryModel,SalaryModel,InvoiceModel,ProjectDetailsModel
from globalApp.models import MonthDataModel
from django.db.models import Count
import datetime
from django.db.models import Q
from django.db.models import Sum,Count
from calendar import weekday, monthrange, SUNDAY,SATURDAY
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
# Create your views here.
def base_view(request):
    total_employee = EmployeeModel.objects.filter(relieving_date=None).count()
    department_wise = DepartmentModel.objects.all().annotate(emp=Count('employeemodel'))
    employee_type_wise = EmployeeTypeModel.objects.all().annotate(emp=Count('employeemodel'))
    
    # print("Department Wise = ",department_wise)
    # print("Employee Wise = ",employee_type_wise)
    # print("Total Employee = ",total_employee)
    context = {
        'department_wise':department_wise,
        'employee_type_wise':employee_type_wise,
        'total_employee':total_employee
    }
    return render(request,'summary_module/index.html',context)

def summary_view(request):
    search = request.POST.get('search')
    summary_month_wise = ''
    if search is not None:
        print('search = ',search,type(search))

        new_date = datetime.datetime.strptime(search, "%Y-%m").date()
        month = new_date.strftime("%b")
        year = new_date.strftime("%Y")
        summary_month_wise = SummaryModel.objects.filter(Q(month=month,year=year))
        print("MONTH WISE DATA = ",summary_month_wise)
        
    summary_data = SummaryModel.objects.all().order_by('-id')
    print("QUERY = ",summary_data)
    # summary_data = SummaryModel.objects.raw('''
    #                                         SELECT * FROM summary_master ORDER BY id DESC''')
    context = {
        'summary_data':summary_data,
        'summary_month_wise':summary_month_wise
    }
    return render(request,'summary_module/summary.html',context)

def add_summary_view(request):
    new_month = ''
    new_year  = ''
    total_headcount = ''
    technical_team = ''
    active_developer=''
    total_working_day = ''
    total_expected_hrs = ''
    total_freeze_hrs = ''
    new_client_hrs = ''
    existing_client_hrs = ''
    total_billable_hrs = ''
    utilization_resources = ''
    project_data = ''
    summary_data_obj = ''
    
    if request.method == 'POST' and 'monthly' in request.POST:
        month = request.POST.get('month')
        month_check = datetime.datetime.strptime(month, "%Y-%m").date()
        new_month = month_check.strftime("%b")
        new_year = month_check.strftime("%Y")
        print("Month = ",new_month," ","YEAR = ",new_year)
        
        print("---- Monthly Data ----")
        # Total Head Count
        total_headcount = EmployeeModel.objects.filter(Q(joining_month=new_month,joining_year=new_year) | Q(relieving_month=new_month,relieving_year=new_year)).count()
        # total_headcount = EmployeeModel.objects.all().count()
        print("TOTAL HEADCOUNT = ",total_headcount)
        
        #Total Technical Team
        technical_team =  EmployeeModel.objects.filter(Q(joining_month=new_month,joining_year=new_year,department__department_name='Operation') | Q(relieving_month=new_month,relieving_year=new_year,department__department_name='Operation')).count()
        print("Technical Team = ",technical_team)
        
        #Total Active Developers
        new_list = []
        active_developer_data = PmSummaryModel.objects.filter(month=new_month,year=new_year)
        for data in active_developer_data:
            if data.submit_flag == True:
                active = data.total_active_developer
                new_list.append(active)
            # else:
            #     print("Not Submit Flag True")
        print("NEW LIST = ",new_list)
        active_developer = sum(new_list)
        print("Total Active Developer = ",active_developer)
        
        # Total Working Days
        date_con = datetime.datetime.strptime(month, "%Y-%m").date()
        month_wise = date_con.strftime("%m")
        # convert str to int 
        converted_month = int(month_wise)
        converted_year = int(new_year)
        # total days
        num_days = monthrange(converted_year,converted_month)[1]
        days = [weekday(converted_year, converted_month, d+1) for d in range(*monthrange(converted_year, converted_month))]
        sunday = days.count(SUNDAY)
        saturday = days.count(SATURDAY)
        #Total Working Days
        total_working_day = num_days-sunday-saturday
        print('Total Working Days = ',total_working_day)
        
        #Total Expected Hours
        total_expected_hrs = total_working_day * 8 * technical_team 
        print('Total Expected Hrs = ',total_expected_hrs)
        
        # project_data = PmSummaryModel.objects.filter(month=new_month,year=new_year).all()
        # print("PROJECT DATA = ",project_data)
        
        #Total Utilization Resources
        utilization_resources_no = active_developer/technical_team*100
        utilization_resources = round(utilization_resources_no,2)
        print('utilization_resources = ',utilization_resources)
        
        print('---- Monthly Data ----')
        
        # Total Freeze Hours
        new_freeze_hrs_list = []
        freeze_hrs_data = PmSummaryModel.objects.filter(month=new_month,year=new_year)
        for data in freeze_hrs_data:
            if data.submit_flag == True:
                freeze_hrs = data.total_freeze_hrs
                print("Total Freeze HOURS = ",type(freeze_hrs),freeze_hrs)
                new_freeze_hrs_list.append(freeze_hrs)
            
        print("LIST FREEZE HOURS = ",new_freeze_hrs_list)
        totalSecs = 0
        for tm in new_freeze_hrs_list:
            timeParts = [int(s) for s in tm.split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        print("%d:%02d" % (hr, min))
        
        total_freeze_hrs = "%d:%02d" % (hr, min)
        print("Total Freeze Hours = ",total_freeze_hrs)
        
        
        # Total New Client Hours
        new_client_hrs_list = []
        freeze_hrs_data = PmSummaryModel.objects.filter(month=new_month,year=new_year)
        for data in freeze_hrs_data:
            if data.submit_flag == True:
                new_client_hrs = data.new_client_hrs
                print("Total New Client HOURS = ",type(new_client_hrs),new_client_hrs)
                new_client_hrs_list.append(new_client_hrs)
            # else:
            #     print("Not Submit Flag True")
            
        print("LIST NEW CLIENT HOURS = ",new_client_hrs_list)
        totalSecs = 0
        for tm in new_client_hrs_list:
            timeParts = [int(s) for s in tm.split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        print("%d:%02d" % (hr, min))
        
        new_client_hrs = "%d:%02d" % (hr, min)
        print("Total New Client Hours = ",new_client_hrs)
        
        
        # Total Existing Client Hours
        exist_client_hrs_list = []
        exist_hrs_data = PmSummaryModel.objects.filter(month=new_month,year=new_year)
        for data in exist_hrs_data:
            if data.submit_flag == True:
                exist_client_hrs = data.existing_client_hrs
                print("Total Existing Client HOURS = ",type(exist_client_hrs),exist_client_hrs)
                exist_client_hrs_list.append(exist_client_hrs)
            
        print("LIST Existing CLIENT HOURS = ",exist_client_hrs_list)
        totalSecs = 0
        for tm in exist_client_hrs_list:
            timeParts = [int(s) for s in tm.split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        print("%d:%02d" % (hr, min))
        
        existing_client_hrs = "%d:%02d" % (hr, min)
        print("Total Exist Client Hours = ",existing_client_hrs)
        
        
        # Total Billable Hours
        billable_hrs_list = []
        billable_hrs_data = PmSummaryModel.objects.filter(month=new_month,year=new_year)
        for data in billable_hrs_data:
            if data.submit_flag == True:
                billable_hrs = data.total_billable_hrs
                print("Total Billable HOURS = ",type(billable_hrs),billable_hrs)
                billable_hrs_list.append(billable_hrs)
            
        print("LIST Billable HOURS = ",billable_hrs_list)
        totalSecs = 0
        for tm in billable_hrs_list:
            print("tm = ",tm)
            timeParts = [int(s) for s in tm.split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        print("%d:%02d" % (hr, min))
        
        total_billable_hrs = "%d:%02d" % (hr, min)
        print("Total Billable Hours = ",total_billable_hrs)
        
        summary_data_obj = SummaryModel.objects.filter(month=new_month,year=new_year).all()
        print("Summary Object = ",summary_data_obj)
            
    else :
        print("NOT POST REQUEST OF MONTHLY")
      
    
    # SAVE FORM
    if request.method == 'POST' and 'saveSummary' in request.POST:
        print("Submit POST")
        flag = request.POST.get('flag')
        flag = False
        print("FLAG SAVE = ",flag)
        
        month = request.POST.get('month')
        year = request.POST.get('year')
        total_headcount = request.POST.get('total_headcount')
        technical_team = request.POST.get('technical_team')
        active_developer = request.POST.get('active_developer')
        total_working_day = request.POST.get('total_working_day')
        total_expected_hrs = request.POST.get('total_expected_hrs')
        total_freeze_hrs = request.POST.get('total_freeze_hrs')
        new_client_hrs = request.POST.get('new_client_hrs')
        existing_client_hrs = request.POST.get('existing_client_hrs')
        total_billable_hrs = request.POST.get('total_billable_hrs')
        total_utilization = request.POST.get('total_utilization')
        total_income = request.POST.get('total_income')
        total_expense = request.POST.get('total_expense')
        profit = request.POST.get('profit')
        per_resource_cost = request.POST.get('per_resource_cost')
        
        summary_data = SummaryModel.objects.create(
            month = month,
            year = year,
            total_headcount = total_headcount,
            technical_team = technical_team,
            active_developer = active_developer,
            total_working_day = total_working_day,
            total_expected_hrs = total_expected_hrs,
            total_freeze_hrs = total_freeze_hrs,
            new_client_hrs = new_client_hrs,
            existing_client_hrs = existing_client_hrs,
            total_billable_hrs = total_billable_hrs,
            total_utilization = total_utilization,
            total_income = total_income,
            total_expense = total_expense,
            profit = profit,
            per_resource_cost = per_resource_cost,
            flag=flag
        )
        print("Save Summary Data = ",summary_data)
        summary_data.save()
        return redirect('/summary')
    else:
        print("Not POST Request")
    
    # SUBMIT FORM CREATE + UPDATE
    if request.method == 'POST' and 'addSummary' in request.POST:
        print("Submit POST")
        id = request.POST.get('id')
        print("UPDATE ID = ",id)
        
        if id :
            print('Update')
            total_headcount = request.POST.get('total_headcount')
            technical_team = request.POST.get('technical_team')
            active_developer = request.POST.get('active_developer')
            total_working_day = request.POST.get('total_working_day')
            total_expected_hrs = request.POST.get('total_expected_hrs')
            total_freeze_hrs = request.POST.get('total_freeze_hrs')
            new_client_hrs = request.POST.get('new_client_hrs')
            existing_client_hrs = request.POST.get('existing_client_hrs')
            total_billable_hrs = request.POST.get('total_billable_hrs')
            total_utilization = request.POST.get('total_utilization')
            total_income = request.POST.get('total_income')
            total_expense = request.POST.get('total_expense')
            profit = request.POST.get('profit')
            per_resource_cost = request.POST.get('per_resource_cost')
            flag = request.POST.get('flag')
            flag = True
            print("FLAG SUBMIT = ",flag)
            print("MONTH = ",total_headcount)
        
            summary = SummaryModel.objects.get(id=id)
            summary.total_headcount = total_headcount
            summary.technical_team = technical_team
            summary.active_developer = active_developer
            summary.total_working_day = total_working_day
            summary.total_expected_hrs = total_expected_hrs
            summary.total_freeze_hrs = total_freeze_hrs
            summary.new_client_hrs = new_client_hrs
            summary.existing_client_hrs = existing_client_hrs
            summary.total_billable_hrs = total_billable_hrs
            summary.total_utilization = total_utilization
            summary.total_income = total_income
            summary.total_expense = total_expense
            summary.profit = profit
            summary.per_resource_cost = per_resource_cost
            summary.flag = flag
            print("SUMMARY = ",summary)
            summary.save()  
            return redirect("/summary")
        else:
            print('Create')
            flag = request.POST.get('flag')
            flag = True        
            month = request.POST.get('month')
            year = request.POST.get('year')
            total_headcount = request.POST.get('total_headcount')
            technical_team = request.POST.get('technical_team')
            active_developer = request.POST.get('active_developer')
            total_working_day = request.POST.get('total_working_day')
            total_expected_hrs = request.POST.get('total_expected_hrs')
            total_freeze_hrs = request.POST.get('total_freeze_hrs')
            new_client_hrs = request.POST.get('new_client_hrs')
            existing_client_hrs = request.POST.get('existing_client_hrs')
            total_billable_hrs = request.POST.get('total_billable_hrs')
            total_utilization = request.POST.get('total_utilization')
            total_income = request.POST.get('total_income')
            total_expense = request.POST.get('total_expense')
            profit = request.POST.get('profit')
            per_resource_cost = request.POST.get('per_resource_cost')
        
            summary_data = SummaryModel.objects.create(
                month = month,
                year = year,
                total_headcount = total_headcount,
                technical_team = technical_team,
                active_developer = active_developer,
                total_working_day = total_working_day,
                total_expected_hrs = total_expected_hrs,
                total_freeze_hrs = total_freeze_hrs,
                new_client_hrs = new_client_hrs,
                existing_client_hrs = existing_client_hrs,
                total_billable_hrs = total_billable_hrs,
                total_utilization = total_utilization,
                total_income = total_income,
                total_expense = total_expense,
                profit = profit,
                per_resource_cost = per_resource_cost,
                flag=flag
            )
            print("Save Summary Data = ",summary_data)
            summary_data.save()
            return redirect('/summary')
    
    else:
        print("Request NOT POST")
    
    
    context = {
        'new_month':new_month,
        'new_year':new_year,
        'total_headcount':total_headcount, 
        'technical_team':technical_team,
        'active_developer':active_developer,
        'total_working_day':total_working_day,  
        'total_expected_hrs':total_expected_hrs,
        'total_freeze_hrs':total_freeze_hrs,
        'new_client_hrs':new_client_hrs,
        'existing_client_hrs':existing_client_hrs,
        'total_billable_hrs':total_billable_hrs,        
        'utilization_resources':utilization_resources,
        'project_data':project_data,
        'summary_data_obj':summary_data_obj,
    }
    return render(request,'summary_module/summaryDetails.html',context)

import calendar
def add_pm_summary_view(request):
    new_month = ''
    new_year = ''
    project_data = ''
    pm_count = ''
    pm_summary_count = ''
    submit_flag =''
    project_manager = ''
    # project_manager = EmployeeModel.objects.filter(employee_type__employee_type='Pm',relieving_date=None)
    pm_summary_data = PmSummaryModel.objects.all()
    
    if request.method == 'POST' and 'monthly' in request.POST:
        month = request.POST.get('month')
        month_check = datetime.datetime.strptime(month, "%Y-%m").date()
        new_month = month_check.strftime("%b")
        new_year = month_check.strftime("%Y")
        print("Month = ",type(new_month)," ","YEAR = ",type(new_year))
        
        project_data = PmSummaryModel.objects.filter(month=new_month,year=new_year).all()
        
        # relieving date filter add
        cov_month = month_check.strftime("%m")
        cov_year = month_check.strftime("%Y")
        con_month = int(cov_month)
        con_year = int(cov_year)
        print("Month = ",con_month,type(con_month)," ","Year = ",con_year,type(con_year))
        res = calendar.monthrange(con_year, con_month)
        day = res[1]
        print(f"Last date of month is: {con_year}-{con_month}-{day}")
        date_var ="{}-{}-{}".format(con_year, con_month,day)
        print("Date Variable = ",date_var,type(date_var))
        rel_date_object = datetime.datetime.strptime(date_var, '%Y-%m-%d').date()
        print("Date Convert = ",type(rel_date_object),rel_date_object.year)
        
        project_manager = EmployeeModel.objects.filter(employee_type__employee_type='Pm').filter(Q(relieving_date__gte=rel_date_object) | Q(relieving_date=None))
        print("Project Manager = ",project_manager)
        
        #show pm count 
        pm_count = EmployeeModel.objects.filter(employee_type__employee_type='Pm').count()
        print("PM Count = ",pm_count)
        # Show pm_summary Objects
        pm_summary_count = PmSummaryModel.objects.filter(month=new_month,year=new_year).count()
        print("PM Summary Count = ",pm_summary_count)
    else:
        print("MONTH IS NONE")
    
    # SAVE BUTTON FORM
    if request.method == 'POST' and 'savePmSummary' in request.POST:
        print("SAVE PM SUMMARY POST")
        
        month = request.POST.get('month')
        year = request.POST.get('year')
        pm_name = request.POST.get('pm_name')
        total_freeze_hrs = request.POST.get('total_freeze_hrs')
        total_billable_hrs = request.POST.get('total_billable_hrs')
        existing_client_hrs = request.POST.get('existing_client_hrs')
        new_client_hrs = request.POST.get('new_client_hrs')
        no_of_resources = request.POST.get('no_of_resources')
        total_active_developer = request.POST.get('total_active_developer')
        pm_flag = request.POST.get('pm_flag')
        pm_flag = True
        submit_flag = request.POST.get('submit_flag')
        submit_flag = False
        
        print("Month = ",month," ","Year = ",year," ","PM FLAG = ",pm_flag," ","SUBMIT FLAG = ",submit_flag)
        print("pm_name = ",pm_name)
        print("total_freeze_hrs = ",total_freeze_hrs)
        print("total_billable_hrs = ",total_billable_hrs)
        print("existing_client_hrs = ",existing_client_hrs)
        print("new_client_hrs = ",new_client_hrs)
        print("no_of_resources = ",no_of_resources)
        print("total_active_developer = ",total_active_developer)
        pm_name = EmployeeModel.objects.get(employee_name=pm_name)
        print("PM NAME ===== ",pm_name)
        
        pm_save_data = PmSummaryModel.objects.filter(month=month,year=year,pm_name=pm_name)
        print("PM SAVE DATA = ",pm_save_data)
        
        if pm_save_data:
            print("Already Exist")
            messages.error(request, 'Pm Already Exist')
        else:
            print("New Create Record")
            create_summary = PmSummaryModel.objects.create(
                month = month,
                year = year,
                pm_name = pm_name,
                total_freeze_hrs = total_freeze_hrs,
                total_billable_hrs = total_billable_hrs,
                existing_client_hrs = existing_client_hrs,
                new_client_hrs = new_client_hrs,
                no_of_resources = no_of_resources,
                total_active_developer = total_active_developer,
                pm_flag = pm_flag,
                submit_flag = submit_flag
            )
            print("Create Summary = ",create_summary)
            create_summary.save()
            return redirect('/addPmSummary')
    else:
        print("NOT POST REQUEST")
    
    # SUBMIT BUTTON FORM
    if request.method == 'POST' and 'addPmSummary' in request.POST:
        print("ADD PM SUMMARY POST")
        
        month = request.POST.get('month')
        year = request.POST.get('year')
        print("MONTH = ",month," ","YEAR = ",year)
        pm_count = EmployeeModel.objects.filter(employee_type__employee_type='Pm').count()
        print("PM Count = ",pm_count)
        pm_summary_count = PmSummaryModel.objects.filter(month=month,year=year).count()
        print("PM Summary Count = ",pm_summary_count)
        
        if pm_count == pm_summary_count:
            pm_summary = PmSummaryModel.objects.filter(month=month,year=year)
            for data in pm_summary:
                
                data.submit_flag = True
                print("After Flag = ",data.submit_flag)
                id = data.id
                month = data.month
                year = data.year
                pm_name = data.pm_name
                total_freeze_hrs = data.total_freeze_hrs
                total_billable_hrs = data.total_billable_hrs
                existing_client_hrs = data.existing_client_hrs
                new_client_hrs = data.new_client_hrs
                no_of_resources = data.no_of_resources
                total_active_developer = data.total_active_developer
                pm_flag = data.pm_flag
                submit_flag = data.submit_flag
                
                print("******* DATA *******")
                print("ID = ",id)
                print("Month = ",month," ","Year = ",year," ","PM FLAG = ",pm_flag," ","SUBMIT FLAG = ",data.submit_flag)
                print("pm_name = ",pm_name)
                print("total_freeze_hrs = ",total_freeze_hrs)
                print("total_billable_hrs = ",total_billable_hrs)
                print("existing_client_hrs = ",existing_client_hrs)
                print("new_client_hrs = ",new_client_hrs)
                print("no_of_resources = ",no_of_resources)
                print("total_active_developer = ",total_active_developer)
                print("******* DATA *******")
                
                pm_summary_obj = PmSummaryModel.objects.get(id=id)
                pm_summary_obj.month = month
                pm_summary_obj.year = year
                pm_summary_obj.pm_name = pm_name
                pm_summary_obj.total_freeze_hrs = total_freeze_hrs
                pm_summary_obj.total_billable_hrs = total_billable_hrs
                pm_summary_obj.existing_client_hrs = existing_client_hrs
                pm_summary_obj.new_client_hrs = new_client_hrs
                pm_summary_obj.no_of_resources = no_of_resources
                pm_summary_obj.total_active_developer = total_active_developer
                pm_summary_obj.pm_flag = pm_flag
                pm_summary_obj.submit_flag = submit_flag
                
                print("SUMMARY = ",pm_summary_obj)
                pm_summary_obj.save()  
            return redirect("/addPmSummary")
        else:
            print("Not Final Submit = ",pm_summary_count)
            messages.error(request, 'Not Submit Other PM Entry is Pending Please Click Save Button')
    
    else:
        print("NOT POST REQUEST CREATE + UPDATE")
        
    context = {
        'new_month':new_month,
        'new_year':new_year,
        'project_manager':project_manager,
        'project_data':project_data,
        'pm_summary_data':pm_summary_data,
        'pm_count':pm_count,
        'pm_summary_count':pm_summary_count,
        'submit_flag':submit_flag
    }
    return render(request,'pm_summary_module/pmSummary.html',context)

# Salary View 
def salary_view(request):
    search = request.POST.get('search') 
    salary_month_wise = ''
    sal_data = ''
    if search is not None:
        print('search = ',search,type(search))

        new_date = datetime.datetime.strptime(search, "%Y-%m").date()
        month = new_date.strftime("%b")
        year = new_date.strftime("%Y")
        monthly_data = MonthDataModel.objects.filter(Q(month=month,year=year))
        print("Monthly Data = ",monthly_data)
        salary_month_wise = SalaryModel.objects.filter(Q(month=month,year=year))
        
        for data in monthly_data:
            print("Working Days = ",data.working_day," ","Per Hour_fix_cost = ",data.per_hrs_fix_cost," ","Dollar Rate = ",data.dollar_rate)
            for sal in salary_month_wise:
                calculate = sal.salary/(data.working_day*8)+data.per_hrs_fix_cost
               
                print("ID = ",sal.id," ","Employee Name = ",sal.employee," ","Salary = ",sal.salary," ","Calculate = ",round(calculate,2))
                per_hrs_cost_inr = round(calculate,2)
                print("INR Rate = ",per_hrs_cost_inr)
                dollar_calculate =  per_hrs_cost_inr/data.dollar_rate
                per_hrs_cost_dollar = round(dollar_calculate,2)
                print("Dollar Rate = ",per_hrs_cost_dollar)
                salary_obj = SalaryModel.objects.get(id=sal.id)
                print("Salary Objects = ",salary_obj)
                salary_obj.month = sal.month
                salary_obj.year = sal.year
                salary_obj.salary = sal.salary
                salary_obj.employee = sal.employee
                salary_obj.payment_mode = sal.payment_mode
                salary_obj.per_hrs_cost_inr = per_hrs_cost_inr
                salary_obj.per_hrs_cost_dollar = per_hrs_cost_dollar
                salary_obj.comments = sal.comments
                
                print("SALARY FINAL = ",salary_obj.per_hrs_cost_inr)
                salary_obj.save()        
                
            # show all data with calculate
            sal_data = SalaryModel.objects.filter(Q(month=month,year=year))
            
    salary_data = SalaryModel.objects.all().order_by('-id')
    # print("QUERY = ",salary_data)
    
    context = {
        'salary_data':salary_data,
        'salary_month_wise':salary_month_wise,
        'sal_data':sal_data
    }
    return render(request,'salary_module/salary.html',context)

#Project Details View
def projects_view(request):
    search = request.POST.get('search')
    project_details_month_wise = ''
    if search is not None:
        print('search = ',search,type(search))

        new_date = datetime.datetime.strptime(search, "%Y-%m").date()
        month = new_date.strftime("%b")
        year = new_date.strftime("%Y")
        project_details_month_wise = ProjectDetailsModel.objects.filter(Q(month=month,year=year))
        print("MONTH WISE DATA = ",project_details_month_wise)
        
    project_details_data = ProjectDetailsModel.objects.all().order_by('-id')
    print("QUERY = ",project_details_data)
    context = {
        'project_details_data':project_details_data,
        'project_details_month_wise':project_details_month_wise
    }
    
    return render(request,'project_insight_module/projects.html',context)

def project_insight_view(request):
    new_month = ''
    new_year  = ''
    project_data = ''
    project_manager = ''
    resource_obj = ''
    
    if request.method == 'POST' and 'monthly' in request.POST:
        month = request.POST.get('month')
        month_check = datetime.datetime.strptime(month, "%Y-%m").date()
        new_month = month_check.strftime("%b")
        new_year = month_check.strftime("%Y")
        print("Month = ",new_month," ","YEAR = ",new_year)
        
        #Project Nama
        project_data = ProjectModel.objects.all()
        # print("Project Name = ",project_data)
        
        #Project Manager Name with reliving date filter add
        cov_month = month_check.strftime("%m")
        cov_year = month_check.strftime("%Y")
        con_month = int(cov_month)
        con_year = int(cov_year)
        print("Month = ",con_month,type(con_month)," ","Year = ",con_year,type(con_year))
        res = calendar.monthrange(con_year,con_month)
        day = res[1]
        print(f"Last date of month is: {con_year}-{con_month}-{day}")
        date_var ="{}-{}-{}".format(con_year, con_month,day)
        print("Date Variable = ",date_var,type(date_var))
        rel_date_object = datetime.datetime.strptime(date_var, '%Y-%m-%d').date()
        print("Date Convert = ",type(rel_date_object),rel_date_object.year)
        #show Project Manger
        project_manager = EmployeeModel.objects.filter(employee_type__employee_type='Pm').filter(Q(relieving_date__gte=rel_date_object) | Q(relieving_date=None))
        # print("Project Manager = ",project_manager)
        
        #Resource Name 
        resource_obj = EmployeeModel.objects.filter(Q(employee_type__employee_type='Developer') | Q(employee_type__employee_type='Qa')).filter(Q(relieving_date__gte=rel_date_object) | Q(relieving_date=None))
        # print("Resource Name = ",resource_name)
            
    else :
        print("NOT POST REQUEST OF MONTHLY")
      
    
    # SAVE FORM
    if request.method == 'POST' and 'saveSalary' in request.POST:
        print("Submit POST")
        
        month = request.POST.get('month')
        year = request.POST.get('year')
        project_name = request.POST.get('project_name')
        project_manager = request.POST.get('project_manager')
        resource_name = request.POST.get('resource_name')
        billable_hrs = request.POST.get('billable_hrs')
        spent_hrs = request.POST.get('spent_hrs')
        per_hrs_cost_inr = request.POST.get('per_hrs_cost_inr')
        per_hrs_cost_dollar = request.POST.get('per_hrs_cost_dollar')
        per_hrs_rate_inr = request.POST.get('per_hrs_rate_inr')
        per_hrs_rate_dollar = request.POST.get('per_hrs_rate_dollar')
        total_cost_inr = request.POST.get('total_cost_inr')
        total_rate_inr = request.POST.get('total_rate_inr')
        total_cost_dollar = request.POST.get('total_cost_dollar')
        total_rate_dollar = request.POST.get('total_rate_dollar')
        profit = request.POST.get('profit')
        
        # print("month = ",month)
        # print("year = ",year)
        # print("project_name = ",project_name)
        # print("project_manager = ",project_manager)
        # print("resource_name = ",resource_name)
        # print("billable_hrs = ",billable_hrs)
        # print("spent_hrs = ",spent_hrs)
        # print("per_hrs_cost_inr = ",per_hrs_cost_inr)
        # print("per_hrs_cost_dollar = ",per_hrs_cost_dollar)
        # print("per_hrs_rate_inr = ",per_hrs_rate_inr)
        # print("per_hrs_rate_dollar = ",per_hrs_rate_dollar)
        # print("total_cost_inr = ",total_cost_inr)
        # print("total_rate_inr = ",total_rate_inr)
        # print("total_cost_dollar = ",total_cost_dollar)
        # print("total_rate_dollar = ",total_rate_dollar)
        # print("profit = ",profit)
        project_details_data = ProjectDetailsModel.objects.create(
            month = month,
            year = year,
            project_name = ProjectModel.objects.get(id=project_name),
            project_manager = EmployeeModel.objects.get(employee_name=project_manager),
            resource_name = EmployeeModel.objects.get(id=resource_name),
            billable_hrs = billable_hrs,
            spent_hrs = spent_hrs,
            per_hrs_cost_inr = per_hrs_cost_inr,
            per_hrs_cost_dollar = per_hrs_cost_dollar,
            per_hrs_rate_inr = per_hrs_rate_inr,
            per_hrs_rate_dollar = per_hrs_rate_dollar,
            total_cost_inr = total_cost_inr,
            total_rate_inr = total_rate_inr,
            total_cost_dollar = total_cost_dollar,
            total_rate_dollar = total_rate_dollar,
            profit = profit,
        )
        print("Save Project Details Data = ",project_details_data)
        project_details_data.save()
        return redirect('/projects')
    else:
        print("Not POST Request")
    
    context = {
        'new_month':new_month,
        'new_year':new_year,
        'project_data':project_data,
        'project_manager':project_manager,
        'resource_obj': resource_obj,
    }
    return render(request,'project_insight_module/project_details.html',context)

# Project_name with Ajax
def ajax_get_val_view(request):
    if request.method == "POST":
        data_id = request.POST.get('edit_id')
        month = request.POST.get('month')
        year = request.POST.get('year')
        # print("Data Id = ",data_id)
        invoice_obj = InvoiceModel.objects.filter(month=month, year=year, project_name=data_id).values()
        # print("invoice_obj = ",invoice_obj)  
        return JsonResponse(list(invoice_obj), safe=False)

# Resource_name with Ajax
def get_resource_view(request):
    if request.method == "POST":
        data_id = request.POST.get('id')
        month = request.POST.get('month')
        year = request.POST.get('year')
        print("Resource Id = ",data_id)
        print("Resource month = ",month)
        print("Resource year = ",year)
        salary_obj = SalaryModel.objects.filter(month=month,year=year,employee=data_id).values()
        print("Salary Object = ",salary_obj)
    return JsonResponse(list(salary_obj), safe=False)