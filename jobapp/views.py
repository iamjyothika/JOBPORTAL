
from rest_framework import generics, status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import  *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination


#  {"email":"asif@gmail.com",
#    "password":"asif00",
#    "username":"Asif",
#    "role":"employer"

#   "email":"jobportal@gmail.com",
#   "password":"jobportal",
#   "username": "Job Portal",
#   "role": "admin"

#  {
#    "email":"careers2024@gmail.com",
#    "password":"careers24",
#    "username":"careerspark",
#    "role":"admin"
#  }
# {"email":"jyothikap@gmail.com",
#     "password":"jyothika13"
# "email":"shamal@gmail.com",
#   "password":"shamal20",
#   "username":"shamal",
#   "role":"employer"

#  "email":"charutha@gmail.com",
#    "password":"charutha04",
#    "username":"Charutha",
#    "role":"candidate"

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes=[AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

       
        user = serializer.validated_data

      
        if user is not None:
           
            login(request, user)
           
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
#retrieves the role of the authenticated person
class RoleView(generics.RetrieveAPIView): 
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
#the authenticated employers create their company    
    
class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
    
        if user.role != 'employer':
            raise ValidationError("Only employers can create a company.")
      
        serializer.save(owner=user)    

class JobListView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  # Employers must be authenticated to post jobs
        return [AllowAny()]  # Anyone can view job listings(admin,candidate, without any authentication)

    
    #search and filtering without authentication
    def get(self, request):
        # Fetch all job listings
        jobs = JobListing.objects.all()
        
        

        # Search by job title
        search_title = request.query_params.get('title', None)
        if search_title:
            jobs = jobs.filter(title__icontains=search_title)
           

        # Search by company name
        search_company = request.query_params.get('company', None)
        if search_company:
            jobs = jobs.filter(company__companyname__icontains=search_company)

        # Search by location
        search_location = request.query_params.get('location', None)
        if search_location:
            jobs = jobs.filter(location__icontains=search_location)

          # Filter by salary greater than or equal to
        # Filter by salary range
        min_salary = request.query_params.get('min_salary', None)
        max_salary = request.query_params.get('max_salary', None)
        
        if min_salary and max_salary:
            jobs = jobs.filter(salary__gte=min_salary, salary__lte=max_salary)
        elif min_salary:
            jobs = jobs.filter(salary__gte=min_salary)
        elif max_salary:
            jobs = jobs.filter(salary__lte=max_salary)
        paginator = PageNumberPagination()
        paginated_jobs = paginator.paginate_queryset(jobs, request)
        serializer = JobListingSerializer(paginated_jobs, many=True)

        return paginator.get_paginated_response(serializer.data)



        # Serialize filtered results
        serializer = JobListingSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployerJobListingsView(APIView):
    def get(self, request):
        # Check if the authenticated user is an employer
        if request.user.role != 'employer':
            return Response({"message": "You have no access to view job listings."}, status=status.HTTP_403_FORBIDDEN)

        # Return job listings where the owner is the authenticated employer
        job_listings = JobListing.objects.filter(owner=request.user)

        if job_listings.exists():
            # If job listings exist, serialize them
            serializer = JobListingSerializer(job_listings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If no job listings exist, return a message
            return Response({"message": "You have not added any job listings."}, status=status.HTTP_200_OK)
        


            
      
        
class CreateJobListingView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        # Only employers can create jobs
        if request.user.role != 'employer':
            return Response({'error': 'Only employers can post jobs.'}, status=status.HTTP_403_FORBIDDEN)

        # Get the company ID from the request data
        company_id = request.data.get('company')

        if not company_id:
            return Response({'error': 'Company ID is required to create a job listing.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure the company belongs to the authenticated employer
            company = Company.objects.get(id=company_id, owner=request.user)
        except Company.DoesNotExist:
            return Response({'error': f'You cannot create jobs for this company (ID: {company_id}).'}, status=status.HTTP_403_FORBIDDEN)

        # Create job listing for the employer's company
        serializer = JobListingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user, company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

   
    

class UpdateJobListingView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, pk):
        try:
            job_listing = JobListing.objects.get(pk=pk, owner=request.user)  # Get job listing for the authenticated employer and update
            serializer = JobListingSerializer(job_listing, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "job listing updated successfully"} ,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except JobListing.DoesNotExist:
            return Response({'detail': 'Job listing not found or you do not have permission to edit this job.'}, status=status.HTTP_404_NOT_FOUND)



    

class DeleteJobListingView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, pk):
        try:
            job_listing = JobListing.objects.get(pk=pk)  # Get the job listing by primary key
            # Check if the user is an admin
            if request.user.role == 'admin':
                job_listing.delete()  # Admin can delete any job listing
                return Response({'detail': 'Job listing deleted successfully.'},status=status.HTTP_204_NO_CONTENT)
            if request.user.role == 'employer' and job_listing.owner == request.user:
                job_listing.delete()  # Employer can delete their own job listing
                return Response({'detail': 'Job listing deleted successfully.'},status=status.HTTP_204_NO_CONTENT)

            return Response({'detail': 'You do not have permission to delete this job listing.'}, status=status.HTTP_403_FORBIDDEN)
        except JobListing.DoesNotExist:
            return Response({'detail': 'Job listing not found.'}, status=status.HTTP_404_NOT_FOUND)
        

 
 

#job application for candidates
class JobApplicationCreateView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure the logged-in user is the candidate
        serializer.save(candidate=self.request.user)


class JobApplicationUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            # Get the job application object for the logged-in candidate
            application = JobApplication.objects.get(pk=pk, candidate=request.user)
            serializer = JobApplicationSerializer(application, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Job application updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JobApplication.DoesNotExist:
            return Response({'detail': 'Job application not found or you do not have permission to update this.'}, status=status.HTTP_404_NOT_FOUND)

class JobApplicationDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            # Get the job application object for the logged-in candidate
            application = JobApplication.objects.get(pk=pk, candidate=request.user)
            application.delete()
            return Response({'detail': 'Job application deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except JobApplication.DoesNotExist:
            return Response({'detail': 'Job application not found or you do not have permission to delete this.'}, status=status.HTTP_404_NOT_FOUND)

class CandidateJobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only job applications for the authenticated candidate
        return JobApplication.objects.filter(candidate=self.request.user)   

class EmployerJobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch the job listings created by the authenticated employer
        employer_jobs = JobListing.objects.filter(owner=self.request.user)
        # Fetch job applications that are associated with those job listings
        return JobApplication.objects.filter(job__in=employer_jobs)



    def delete(self, request, *args, **kwargs):
        # Get the specific job application
        job_application_id = kwargs.get('pk')
        try:
            # Ensure that the employer owns the job listing related to the job application
            job_application = JobApplication.objects.get(id=job_application_id)
            if job_application.job.owner == request.user:
                # Employer owns the job listing, so they can delete the job application
                job_application.delete()
                return Response({"detail": "Job application deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                # Employer does not own the job listing, return unauthorized
                return Response({"detail": "You are not authorized to delete this job application."}, status=status.HTTP_403_FORBIDDEN)
        except JobApplication.DoesNotExist:
            return Response({"detail": "Job application not found."}, status=status.HTTP_404_NOT_FOUND)
        
    

class EmployerCandidateDetails(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    def get(self, request):
        if request.user.role == "admin":
            candidates = User.objects.filter(role='candidate').values('id', 'username', 'email')
            
            # Get all employers and their company details
            employers_with_companies = Company.objects.select_related('owner').values(
                'companyname', 'location', 'description', 'owner__username', 'owner__email'
            )

            # Format response data
            response_data = {
                'candidates': list(candidates),
                'employers': list(employers_with_companies),
            }
            
            return Response(response_data, status=200)
        else:
            return Response({'detail': 'Permission denied'}, status=403)
           
    
class AdminJobApplications(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    def get(self, request):
        if request.user.role.lower() == "admin":  # Ensure case-insensitivity
            job_applications = JobApplication.objects.all()
            print(job_applications)
            serializer = JobApplicationSerializer(job_applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            # paginator = PageNumberPagination()
            # paginator.page_size = 1 # Set the number of applications per page
            # paginated_job_applications = paginator.paginate_queryset(job_applications, request)

            # # Serialize the paginated results
            # serializer = JobApplicationSerializer(paginated_job_applications, many=True)

            # # Return paginated response
            # return paginator.get_paginated_response(serializer.data)
        return Response({"message": "Authenticated user is not an admin"}, status=status.HTTP_403_FORBIDDEN)
    
class ApproveRejectJobApplicationView(generics.UpdateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes=[JWTAuthentication] # Only allow admins to access this view

    def patch(self, request, *args, **kwargs):
        # Get the application instance
        job_application = self.get_object()  # Get the job application instance based on the provided ID
        action = request.data.get('action')
     
        
        # Check if the user is an admin
        if request.user.role != 'admin':
            return Response(
                {"detail": "Only admins can approve or reject applications."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Update the application status
      
        if action == 'accepted':
            if job_application.status == "Rejected":
                return Response({
                    'message': 'This application has been rejected and cannot be approved again. Please ask the candidate to reapply.'
                }, status=status.HTTP_400_BAD_REQUEST)

            job_application.status = 'Accepted'  # Update status to accepted
            message = 'Application approved successfully.'
        elif action == 'reject':
            job_application.status = 'Rejected'  # Update status to rejected
            message = 'Application rejected successfully.'
        else:
            return Response({'error': 'Invalid operation. Use "approve" or "reject".'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated job application status
        job_application.save()
        serializer = JobApplicationSerializer(job_application)  # Serialize the updated job application instance

        return Response({
            'message': message,
            'application': serializer.data
        }, status=status.HTTP_200_OK)

    def get_object(self):
        # Override this method to get the JobApplication instance based on the provided ID
        application_id = self.kwargs.get('pk')  # Assuming the application ID is passed as a URL parameter
        return JobApplication.objects.get(id=application_id)