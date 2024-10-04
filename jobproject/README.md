# Job Portal API

This project is a Job Portal API built with Django and Django REST Framework. The API allows employers to create and manage job listings, and candidates to apply for jobs.

## Features
- Employers can create their company
- Employers can create, update, and delete job listings for their company.
- Candidates can apply to job listings with a resume and cover letter and can make updations in their applications.Also given the deleting rights
- Employers can view applications for their job listings and delete applications.
- JWT authentication for users (Employers Candidates and admins).
- Admin can  view the details of candidates and employers.
- Admin can approve or reject the candidate applications that is pending

---

## Table of Contents

1. [Project Setup](#project-setup)
2. [Authentication](#authentication)
3. [API Documentation](#api-documentation)
   - [Employer Endpoints](#employer-endpoints)
   - [Candidate Endpoints](#candidate-endpoints)
   -[Admin Endpoints](#Admin-endpoints)
4.[Conclusion]

## Project Setup

### Prerequisites

- Python 3.x
- Django 4.x
- Django REST Framework
- db.sqlite3(default database)

### Installation Steps

1. **Clone the repository**:

   
   git clone https://github.com/iamjyothika/JOBPORTAL.git
   cd JOBPORTAL

Run migrations:
python manage.py migrate

Create a superuser:(Django admin)
python manage.py createsuperuser

Start the server:
python manage.py runserver
The API will be running at http://127.0.0.1:8000/.



# Authentication
This API uses JWT (JSON Web Token) for authentication. To authenticate, you need to obtain a JWT token by sending a POST request with valid credentials.

Obtain Token
Endpoint: /login/


POST /login/
Content-Type: application/json

{
    "email": "user123",
    "password": "password123"
}
Response
{
    "access": "your-access-token",
    "refresh": "your-refresh-token"
} 

Usage
include the token in the Authorization header in all API requests that require authentication:

Authorization: Bearer your-access-token



# API DOCUMENTATION

# Employer Endpoints
Create Company
URL: /create-company/
Method: POST
Auth: JWT Token (employer only)
Request Body:

json

{ "companyname": "Softronics",
    "location": "Calicut",
  
 "description":"Softronics delivers advanced technology solutions, empowering businesses to optimize their operations and reach their objectives through innovative software development and expert IT consulting."
}
Response-Json
{
  "companyname": "Softronics",
  "location": "Calicut",
  "description": "Softronics delivers advanced technology solutions, empowering businesses to optimize their operations and reach their objectives through innovative software development and expert IT consulting.",
  "owner": 8
}

Create Job Listing

URL: /api/jobs/create/
Method: POST
Auth: JWT Token (employer only)

Request Body:

json
{
  
    "title": "Senior Backend Developer",
    "company": 4,
    "description": "Responsible for designing and developing APIs.",
    "requirements": "5+ years of experience with Django and REST framework.",
    "location": "Thrissur",
    "salary": 120000
}


Response:

json
{
  "id": 9,
  "title": "Senior Backend Developer",
  "company": 4,
  "company_name": "TechCorp",
  "description": "Responsible for designing and developing APIs.",
  "requirements": "5+ years of experience with Django and REST framework.",
  "location": "Thrissur",
  "salary": 120000,
  "created_at": "2024-10-04T06:26:26.906000Z",
  "is_active": true
}

Note: Only users with the role employer can create job listings.


View the job listings they have created (for employers only)
URL: /employer/job-listings/
Method: GET
Auth: JWT Token (employer only)

Response
[
  {
    "id": 4,
    "title": "Software Engineer",
    "company": 1,
    "company_name": "Tech Solutions",
    "description": "We are looking for a Software Engineer to develop and maintain software applications.",
    "requirements": "Experience in Python and Django.",
    "location": "Calicut",
    "salary": 80000,
    "created_at": "2024-10-02T06:45:04.458178Z",
    "is_active": true
  },
  {
    "id": 8,
    "title": "Senior Python-django Developer",
    "company": 1,
    "company_name": "Tech Solutions",
    "description": "Responsible for designing and developing applications using python and django.",
    "requirements": "2+ years of experience with Django and Django",
    "location": "Calicut",
    "salary": 150000,
    "created_at": "2024-10-04T06:14:53.551652Z",
    "is_active": true
  }
]


Get Job Applications

URL: /candidate-applications/
Method: GET
Auth: JWT Token (employer only)

Response:

json

{
      "id": 1,
      "job": 3,
      "candidate_name": "jyothika",
      "resume": "http://127.0.0.1:8000/media/resumes/jyothikaptresume13.pdf",
      "cover_letter": "Dear Hiring Manager, I am writing to express my interest in the Mern Stack Developer Position at  Innovative Web Services. With my skills in [specific skill related to the job], I am confident that I would make a valuable contribution to your team. I am excited about the opportunity to bring my expertise to [Company Name] and contribute to its continued success. Thank you for considering my application. I look forward to the opportunity to discuss how my background aligns with the needs of your team. Sincerely, Jyothika",
      "applied_at": "2024-10-02T15:04:43.330618Z",
      "status": "Accepted"
    },
    {
      "id": 3,
      "job": 3,
      "candidate_name": "Charutha",
      "resume": "http://127.0.0.1:8000/media/resumes/devikacv.pdf",
      "cover_letter": "please find my resume",
      "applied_at": "2024-10-02T17:08:38.584125Z",
      "status": "pending"
    }


Updating job listing 
URL:/jobs/update/<int:pk>/
Method: Patch
Auth: JWT Token (employer only)



Body-Json
{
  "requirements":" 1 year Experience in full-stack development using MongoDB, Express.js, React.js, and Node.js. Strong understanding of JavaScript, HTML, and CSS."
}

Response
{
  "message": "job listing updated successfully"
}


Delete Job Application

URL: /delete/applications/<int:pk>/
Method: DELETE
Auth: JWT Token (employer only)



# Candidate endpoints
Endpoint: POST /api/jobapply/
Description: Allows candidates to apply for a job by submitting their resume and cover letter. Only authenticated users with the role candidate can apply.

Request:
json

{
    "job": 1,
    "resume": "path/to/resume.pdf",
    "cover_letter": "I am interested in this position."
}
job: The ID of the job listing the candidate is applying to.
resume: The file path or base64 string of the resume file.
cover_letter: (optional) A text description provided by the candidate.
Response:
json
{
    "id": 6,
    "job": 4,
    "candidate_name": "jyothika",
    "resume": "http://127.0.0.1:8000/media/resumes/Screenshot_2024-10-03_001403.png",
    "cover_letter": "i am interested",
    "applied_at": "2024-10-04T08:28:16.189470Z",
    "status": "pending"
}
Note: Only candidates (users with the role candidate) can apply.


2. Update a Job Application
Endpoint: PATCH /api/applications/{application_id}/update/
Description: Allows candidates to update an existing job application (e.g., change resume or cover letter). Only authenticated candidates who created the application can perform this action.

Request:
json

{
    "resume": "path/to/new_resume.pdf",
    "cover_letter": "I have updated my cover letter for this position."
}
resume: (optional) The file path or base64 string of the updated resume file.
cover_letter: (optional) The updated cover letter text.
Response:
json
C
{
    "detail": "Job application deleted successfully."
}
the changes will  reflected in the database

Note: Only candidates who submitted the application can update it.

3. Delete a Job Application
Endpoint: DELETE /api/applications/{application_id}/delete/
Description: Allows candidates to delete an existing job application. Only the candidate who submitted the application can delete it.

Response:
json

{
    "detail": "Job application deleted successfully."
}
Note: Candidates can only delete their own applications.

4. View Candidate's Job Applications
Endpoint: GET /api/my-applications/
Description: Retrieves all job applications submitted by the authenticated candidate.

Response:
json
Copy code
[
    {
        "id": 1,
        "job": {
            "id": 1,
            "title": "Software Developer",
            "company_name": "Tech Solutions"
        },
        "resume": "path/to/resume.pdf",
        "cover_letter": "I am interested in this position.",
        "applied_at": "2024-10-03T12:34:56Z",
        "status": "pending"
    },
    {
        "id": 2,
        "job": {
            "id": 2,
            "title": "Data Analyst",
            "company_name": "Data Innovations"
        },
        "resume": "path/to/resume.pdf",
        "cover_letter": "I have a passion for data analytics.",
        "applied_at": "2024-10-04T14:22:33Z",
        "status": "pending"
    }
]
This will return a list of job applications where each object includes the job details, resume, cover letter, and status.
Only the logged-in candidate will be able to view their applications.
Authentication
All endpoints require JWT authentication. Include the following header in your requests:



Authorization: Bearer <your_access_token>(candidate access token)



Error Handling
401 Unauthorized: If the user is not authenticated.
403 Forbidden: If the user tries to access or modify another user's applications.
404 Not Found: If the job application or job listing is not found.


# Admin endpoints


1. View Employer-Candidate Details
Endpoint: GET /api/employee-candidate/details/
Description: Allows admins to view details of the employer and their company and the candidates 

Response:
{
  "candidates": [
    {
      "id": 4,
      "username": "jyothika",
      "email": "jyothikap@gmail.com"
    },
    {
      "id": 6,
      "username": "Charutha",
      "email": "charutha@gmail.com"
    }
  ],
  "employers": [
    {
      "companyname": "Tech Solutions",
      "location": "Calicut",
      "description": "We provide tech solutions for startups.",
      "owner__username": "kashyap",
      "owner__email": "kashyap@gmail.com"
    },
    {
      "companyname": "Innovative Web Services",
      "location": "Calicut",
      "description": "A web development company specializing in cutting-edge solutions for e-commerce platforms and online businesses.",
      "owner__username": "shamal",
      "owner__email": "shamal@gmail.com"
    },
    {
      "companyname": "Hamon Technologies",
      "location": "Kochi",
      "description": "Hamon Technologies is a leading provider of innovative technology solutions, dedicated to helping businesses streamline their operations and achieve their goals through cutting-edge software development and IT consulting.",
      "owner__username": "Christo",
      "owner__email": "christo@gmail.com"
    },
    {
      "companyname": "TechCorp",
      "location": "Thrissur",
      "description": "TechCorp is a dynamic technology company specializing in delivering custom software solutions and IT services to businesses of all sizes. Our mission is to empower organizations with innovative tools and strategies that enhance productivity and drive growth.",
      "owner__username": "Asif",
      "owner__email": "asif@gmail.com"
    }
  ]
}

2. View All Job Applications
Endpoint: GET /api/super/applications/
Description: Allows admins to view all job applications across all job listings. Admins have full visibility of all applications made in the system.

Response:
[
  {
    "id": 1,
    "job": 3,
    "candidate_name": "jyothika",
    "resume": "/media/resumes/jyothikaptresume13.pdf",
    "cover_letter": "Dear Hiring Manager, I am writing to express my interest in the Mern Stack Developer Position at  Innovative Web Services. With my skills in [specific skill related to the job], I am confident that I would make a valuable contribution to your team. I am excited about the opportunity to bring my expertise to [Company Name] and contribute to its continued success. Thank you for considering my application. I look forward to the opportunity to discuss how my background aligns with the needs of your team. Sincerely, Jyothika",
    "applied_at": "2024-10-02T15:04:43.330618Z",
    "status": "Accepted"
  },
  {
    "id": 3,
    "job": 3,
    "candidate_name": "Charutha",
    "resume": "/media/resumes/devikacv.pdf",
    "cover_letter": "please find my resume",
    "applied_at": "2024-10-02T17:08:38.584125Z",
    "status": "pending"
  },
  {
    "id": 5,
    "job": 4,
    "candidate_name": "Charutha",
    "resume": "/media/resumes/Jyothika_Resume_1_uek5qAj.pdf",
    "cover_letter": "I am confident in my skills.Yours sincerly charutha",
    "applied_at": "2024-10-03T17:00:52.164330Z",
    "status": "pending"
  },
  {
    "id": 6,
    "job": 4,
    "candidate_name": "jyothika",
    "resume": "/media/resumes/Screenshot_2024-10-03_001403.png",
    "cover_letter": "i am interested",
    "applied_at": "2024-10-04T08:28:16.189470Z",
    "status": "pending"
  }
]

Approve or Reject a Job Application
Method: PATCH /api/super/applications/{application_id}/approve-reject/
Description: Allows admins to approve or reject a job application by changing its status. Admins can set the status to either accepted or rejected.

Request:
json

{
    "action": "accepted"
}
action: The new status of the job application. Allowed values: accepted, rejected.

Response:
{
  "message": "Application approved successfully.",
  "application": {
    "id": 1,
    "job": 3,
    "candidate_name": "jyothika",
    "resume": "/media/resumes/jyothikaptresume13.pdf",
    "cover_letter": "Dear Hiring Manager, I am writing to express my interest in the Mern Stack Developer Position at  Innovative Web Services. With my skills in [specific skill related to the job], I am confident that I would make a valuable contribution to your team. I am excited about the opportunity to bring my expertise to [Company Name] and contribute to its continued success. Thank you for considering my application. I look forward to the opportunity to discuss how my background aligns with the needs of your team. Sincerely, Jyothika",
    "applied_at": "2024-10-02T15:04:43.330618Z",
    "status": "Accepted"
  }
}


without authentication and without authentication

To view all job listings
Endpoint: GET /api/jobs/

Response:[
        {
            "id": 3,
            "title": "MERN Stack Developer",
            "company": 2,
            "company_name": "Innovative Web Services",
            "description": "Responsible for developing and maintaining web applications using the MERN stack (MongoDB, Express.js, React.js, Node.js).",
            "requirements": "1 year Experience in full-stack development using MongoDB, Express.js, React.js, and Node.js. Strong understanding of JavaScript, HTML, and CSS.",
            "location": "Calicut",
            "salary": 60000,
            "created_at": "2024-10-02T06:42:50.140142Z",
            "is_active": true
        },
        {
            "id": 4,
            "title": "Software Engineer",
            "company": 1,
            "company_name": "Tech Solutions",
            "description": "We are looking for a Software Engineer to develop and maintain software applications.",
            "requirements": "Experience in Python and Django.",
            "location": "Calicut",
            "salary": 80000,
            "created_at": "2024-10-02T06:45:04.458178Z",
            "is_active": true
        }
 {
            "id": 8,
            "title": "Senior Python-django Developer",
            "company": 1,
            "company_name": "Tech Solutions",
            "description": "Responsible for designing and developing applications using python and django.",
            "requirements": "2+ years of experience with Django and Django",
            "location": "Calicut",
            "salary": 150000,
            "created_at": "2024-10-04T06:14:53.551652Z",
            "is_active": true
        },
        {
            "id": 9,
            "title": "Senior Backend Developer",
            "company": 4,
            "company_name": "TechCorp",
            "description": "Responsible for designing and developing APIs.",
            "requirements": "5+ years of experience with Django and REST framework.",
            "location": "Thrissur",
            "salary": 120000,
            "created_at": "2024-10-04T06:26:26.906000Z",
            "is_active": true
        }
]


searching and filtering using keywords(without authentication)
Method GET /api/jobs/?title=Developer
Response:
[
        {
            "id": 3,
            "title": "MERN Stack Developer",
            "company": 2,
            "company_name": "Innovative Web Services",
            "description": "Responsible for developing and maintaining web applications using the MERN stack (MongoDB, Express.js, React.js, Node.js).",
            "requirements": "1 year Experience in full-stack development using MongoDB, Express.js, React.js, and Node.js. Strong understanding of JavaScript, HTML, and CSS.",
            "location": "Calicut",
            "salary": 60000,
            "created_at": "2024-10-02T06:42:50.140142Z",
            "is_active": true
        },
        {
            "id": 8,
            "title": "Senior Python-django Developer",
            "company": 1,
            "company_name": "Tech Solutions",
            "description": "Responsible for designing and developing applications using python and django.",
            "requirements": "2+ years of experience with Django and Django",
            "location": "Calicut",
            "salary": 150000,
            "created_at": "2024-10-04T06:14:53.551652Z",
            "is_active": true
        }
        {
            "id": 9,
            "title": "Senior Backend Developer",
            "company": 4,
            "company_name": "TechCorp",
            "description": "Responsible for designing and developing APIs.",
            "requirements": "5+ years of experience with Django and REST framework.",
            "location": "Thrissur",
            "salary": 120000,
            "created_at": "2024-10-04T06:26:26.906000Z",
            "is_active": true
        }
    ]



# Conclusion
The API endpoints detailed in this documentation provide a comprehensive solution for managing job applications within your application. Admins have the necessary tools to view employer-candidate details, oversee all job applications, and approve or reject applications, ensuring a streamlined workflow in the recruitment process.

Key Features:
Admin Control: Administrators can access all job applications, making it easy to track and manage candidate submissions.
Candidate Insights: The ability to view candidate names and application details facilitates informed decision-making for job listings.
Approval Workflow: The approval and rejection of applications streamline the hiring process, enabling quick responses to candidates.
By implementing these endpoints, your application enhances the recruitment experience for both candidates and employers, fostering a more efficient hiring process. Ensure that authentication measures are upheld to maintain data integrity and secure sensitive information throughout the API interactions.