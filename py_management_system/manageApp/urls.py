from . import views as user_views
from django.urls import path
app_name = 'manageApp'

urlpatterns = [
    # path('/import_excel', user_views.index_view, name='index'),
    path('', user_views.base_view, name='base_view'),
    path('summary', user_views.summary_view, name='summary_view'),
    path('addSummary', user_views.add_summary_view, name='add_summary_view'),
    path('addPmSummary', user_views.add_pm_summary_view, name='add_pm_summary_view'),
    #Salary Module URL 
    path('salary', user_views.salary_view, name='salary_view'),
    
    #Project Module URL
    path('projects', user_views.projects_view, name='projects'),
    path('project_details', user_views.project_insight_view, name='project_insight_view'),
    path('ajax/get/val/', user_views.ajax_get_val_view, name='ajax_get_val'),
    path('ajax/get/resource', user_views.get_resource_view, name='get_resource')
]