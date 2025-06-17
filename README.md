# HR System API - Version 1.0

**This repository contains the backend API for a modern Human Resource Management System. Built with Django and Django REST Framework, this robust and scalable API provides the core functionalities needed to streamline HR processes and improve employee management within an organization.**

**The system is designed to be containerized with Docker, making local development and production deployment simple and consistent.**

## Features
The HR System API includes the following core modules:

* 👤 User Authentication: Secure user registration and authentication using JSON Web Tokens (JWT) with access and refresh tokens.

* 👥 Employee Onboarding: Full CRUD (Create, Read, Update, Delete) functionality for managing detailed employee profiles. Profiles are automatically created upon user registration and can be updated by an HR administrator.

* 🕒 Attendance Tracking: Endpoints for employees to clock-in and clock-out, automatically calculating the work duration.

* 🌴 Leave Management: A complete workflow for employees to request leave and for administrators to approve or reject those requests.

* 📊 Reporting & Analytics:

    * An admin-only dashboard endpoint that provides key HR metrics, such as total employee count and department distribution.

    * Functionality to export a full employee list as a downloadable .csv file.

## Technology Stack
**Backend:** Django, Django REST Framework

**Database:** PostgreSQL

**Authentication:** djangorestframework-simplejwt (Access & Refresh Tokens)

**API Documentation:** drf-yasg (Swagger UI / ReDoc)

**CORS:** django-cors-headers

**Containerization:** Docker, Docker Compose

# API Endpoints Overview
The API is versioned under ```/api/v1/```.
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/register/` | `POST` | Register a new user. |
| `/login/` | `POST` | Log in to receive access and refresh JWTs. |
| `/login/refresh/` | `POST` | Refresh an expired access token. |
| `/employees/` | `GET`, `PATCH`, `DELETE` | List, update, or delete employee profiles (Admin). |
| `/attendance/clock-in/` | `POST` | Clock in for the current day. |
| `/attendance/clock-out/` | `POST` | Clock out for the current day. |
| `/leaves/` | `GET`, `POST` | List your leave requests or create a new one. |
| `/leaves/{id}/approve/` | `POST` | Approve a leave request (Admin). |
| `/leaves/{id}/reject/` | `POST` | Reject a leave request (Admin). |
| `/reports/dashboard-summary/` | `GET` | Get key HR metrics (Admin). |
| `/reports/export/employees/` | `GET` | Download an employee report as a CSV file (Admin). |

# Local Development Setup

This project is configured to run locally using Docker and Docker Compose for a consistent and isolated development environment.
### Prerequisites
* Docker installed on your local machine.

### Configuration
1. **Clone the Repository:**
```
git clone <your-repository-url>
cd <your-project-folder>
```
2. **Create the Environment File:**
    * Create a file named .env.dev in the project root.

    * Add your environment-specific variables. This file is ignored by Git.
```
# .env.dev
DEBUG=1
SECRET_KEY=your_django_secret_key_goes_here
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DATABASE_URL=postgresql://your_db_user:your_db_password@your_db_host/your_db_name
```
3. **Create a Superuser (Admin Account):**
```
docker-compose run --rm web python manage.py createsuperuser
```
4. **Start the Server:**
```
docker-compose up
```
The application will be running and accessible at ```http://localhost:8000```. The API documentation can be found at ```http://localhost:8000/swagger/```.

# Running Automated Tests

The project includes a comprehensive test suite to ensure API reliability. To run the tests, execute the following command:
```
python manage.py test
```
# Visit the live backend On:
## **click**--> [Render](https://hr-system-0whu.onrender.com/swagger/)