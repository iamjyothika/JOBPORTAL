
from rest_framework import generics, status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import UserRegistrationSerializer, UserLoginSerializer, RoleSerializer,JobListingSerializer,CompanySerializer,JobApplicationSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from urllib.parse import unquote
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


        # Serialize filtered results
        serializer = JobListingSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployerJobListingsView(generics.ListAPIView):
    serializer_class = JobListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return job listings where the owner is the authenticated employer
        return JobListing.objects.filter(owner=self.request.user)   
        


            
      
        

    def post(self, request):
        # Only employers can create jobs
        if request.user.role != 'employer':
            return Response({'error': 'Only employers can post jobs.'}, status=status.HTTP_403_FORBIDDEN)

        # Create job listing
        serializer = JobListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    


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
    



    

