from django.urls import path,include
from .views import *
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('role/', RoleView.as_view(), name='role'),
    path('create-company/', CompanyCreateView.as_view(), name='create-company'),
    path('jobs/', JobListView.as_view(), name='job-list'),#without or with  authentication anyone can see the joblistings

    path('employer/job-listings/', EmployerJobListingsView.as_view(), name='employer-job-listings'),#authenticated employer can view their job listings they have added
    path('jobs/<int:pk>/', JobListView.as_view(), name='job-detail'),#for the authenticated employer-updating and deleting  the job listings they have added 
    

    
    #candidates can access their applications
    path('jobapply/', JobApplicationCreateView.as_view(), name='create-job-application'),
    path('applications/<int:pk>/update/', JobApplicationUpdateView.as_view(), name='job-application-update'),
    path('applications/<int:pk>/delete/', JobApplicationDeleteView.as_view(), name='job-application-delete'),
    path('my-applications/', CandidateJobApplicationsView.as_view(), name='my-job-applications'),


    path('candidates-applications/', EmployerJobApplicationsView.as_view(), name='employer-job-applications'),#employer can view the applications applied for the job listing they have posted
     path('delete/applications/<int:pk>/', EmployerJobApplicationsView.as_view(), name='delete-job-application'),#employer can delete the applications applied for the job listing they have posted

   
   
   #admin access to applications
    # path('admin/applications/', AdminJobApplicationsView.as_view(), name='admin-job-applications'),

    
    
   








]