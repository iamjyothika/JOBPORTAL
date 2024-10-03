from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

  

    def __str__(self):
        return self.username

class Company(models.Model):
    companyname=models.CharField(max_length=100) 
    location=models.CharField(max_length=100) 
    description=models.TextField() 
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    def clean(self):
        
        if self.owner and self.owner.role != 'employer':
            raise ValidationError("The owner must have the Employer role.")
    
    def __str__(self):
        return self.companyname
    
class JobListing(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_listings',null=True)  

    def __str__(self):
        return self.title  

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)  
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def clean(self):
        
        if self.candidate and self.candidate.role != 'candidate':
            raise ValidationError("Only users with the Candidate role can apply for jobs.")
    
    def __str__(self):
        return f'{self.candidate.username} - {self.job.title}'      

