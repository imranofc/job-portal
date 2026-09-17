# JobPortal

A full-stack job portal built with **Django** that connects job seekers with employers. Users can discover job opportunities, filter listings, apply with their resumes, while employers can create and manage job postings and track job views and applications.

## Live Demo

**Live Website:** https://job-portal.imranofc.com/

**GitHub Repository:** https://github.com/imranofc/job-portal

## Features

### Job Seekers

* Create an account as a Job Seeker
* Secure login and logout
* Browse available job opportunities
* Search jobs by location
* Filter jobs by:

  * Location
  * Job Type
  * Category
* View complete job details
* Apply for jobs with:

  * Name
  * Email
  * Phone number
  * Resume upload
* Track job opportunities through the job listing interface
* Automatic job view tracking
* Password reset functionality

### Employers

* Create an account as an Employer
* Employer-specific dashboard
* Post new job opportunities
* Add job information such as:

  * Job title
  * Company
  * Description
  * Location
  * Category
  * Job Type
  * Application method
* Choose between:

  * Resume-based applications
  * External application link
* View jobs posted by the employer
* Manage individual job postings
* View job statistics
* Track the number of job views
* Track received applications
* View people who viewed a job
* View applications received for a job
* Edit job postings
* Pause/deactivate job postings

### Authentication

* User registration
* Email-based login
* Role-based access
* Session-based authentication
* Password validation
* Forgot password functionality
* Secure password reset tokens
* Access protection for employer and job-seeker features

### User Roles

The application supports two primary roles:

* **Job Seeker**
* **Employer**

Role-based access ensures that users are redirected to the appropriate areas of the application.

## Tech Stack

| Layer                | Technology                         |
| -------------------- | ---------------------------------- |
| Backend              | Django                             |
| Programming Language | Python                             |
| Database             | SQLite                             |
| Frontend             | Django Templates                   |
| Styling              | HTML & CSS                         |
| JavaScript           | Vanilla JavaScript                 |
| Icons                | Font Awesome                       |
| Fonts                | Google Fonts - Inter               |
| Authentication       | Django Authentication              |
| File Uploads         | Django Media Files                 |
| Email                | Django Email Backend               |
| Deployment           | Django + Gunicorn/Nginx compatible |

<!-- Baaki README bilkul same rahega -->
