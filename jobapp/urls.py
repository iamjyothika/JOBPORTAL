from django.urls import path,include
from .views import *
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('role/', RoleView.as_view(), name='role'),
    path('create-company/', CompanyCreateView.as_view(), name='create-company'),
    path('jobs/', JobListView.as_view(), name='job-list'),#without or with  authentication anyone can see the joblistings

    path('employer/job-listings/', EmployerJobListingsView.as_view(), name='employer-job-listings'),#authenticated employer can view their job listings they have added
    path('jobs/create/', CreateJobListingView.as_view(), name='create-job-listing'),# authenticated employer can create the job listing
    path('jobs/update/<int:pk>/', UpdateJobListingView.as_view(), name='update-job-listing'),#for the authenticated employer-updating the job listings they have added
    path('jobs/delete/<int:pk>/', DeleteJobListingView.as_view(), name='delete-job-listing'),#for the authenticated employer-deleting the job listings they have added
    
     
    

    
    #candidates can access their applications
    path('jobapply/', JobApplicationCreateView.as_view(), name='create-job-application'),
    path('applications/<int:pk>/update/', JobApplicationUpdateView.as_view(), name='job-application-update'),
    path('applications/<int:pk>/delete/', JobApplicationDeleteView.as_view(), name='job-application-delete'),
    path('my-applications/', CandidateJobApplicationsView.as_view(), name='my-job-applications'),

  #employee access to candidate applications
    path('candidates-applications/', EmployerJobApplicationsView.as_view(), name='employer-job-applications'),#employer can view the candidate applications  for the job listing they have posted
     path('delete/applications/<int:pk>/', EmployerJobApplicationsView.as_view(), name='delete-job-application'),#employer can delete the candidate applications  for the job listing they have posted

   
   
   #admin access to applications and view the employers-candidate details
    path('employee-candidate/details/', EmployerCandidateDetails.as_view(), name='admin-details'),
    path('super/applications/', AdminJobApplications.as_view(), name='admin-job-applications'),#viewing all applications
    path('super/applications/<int:pk>/approve-reject/', ApproveRejectJobApplicationView.as_view(), name='approve-reject-job-application'),#approve/reject applications

    
    
   








]