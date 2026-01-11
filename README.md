Django Task Manager Backend API

A backend REST API built using Django and Django REST Framework that supports task management with role-based access control, filtering, audit logging, and background job processing using Celery + Redis.

This project was developed as part of a Django Backend Internship Technical Evaluation.

 Core Features:

Task CRUD operations

JWT-based authentication

Role-based access control (ADMIN / INTERN)

Pagination, filtering, sorting

Activity logging (audit trail)

Overdue task automation (background job)

 Advanced Features:

Background task scheduling using Celery Beat

Redis as message broker

Audit logs for task updates, deletions, and status changes

 Tech Stack:

Python 3

Django

Django REST Framework

SimpleJWT (Authentication)

django-filter

Celery

Redis

Docker (for Redis)

📁 Project Structure (Simplified)
config/
│
├── config/                # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── __init__.py
│
├── tasks/                 # Task management app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tasks_celery.py
│   └── admin.py
|
|── user/                  # user app
│
├── venv/                  # Virtual environment 
├── manage.py
└── README.md

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone <your-repo-url>
cd config

2️⃣ Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-filter
pip install celery
pip install redis

4️⃣ Run Database Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Create Superuser (Admin)
python manage.py createsuperuser

6️⃣ Start Redis (Using Docker)
docker run -d -p 6379:6379 redis

7️⃣ Run the Application
Terminal 1 — Django Server
python manage.py runserver

Terminal 2 — Celery Worker
celery -A config worker -l info -P solo

Terminal 3 — Celery Beat (Scheduler)
python -m celery -A config beat -l info

🔐 Authentication Flow (JWT)
Login
POST /api/auth/login/


--Request Body--

{
  "username": "admin",
  "password": "password"
}

          |
          |
          |
         \_/

--Response--

{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}


Use the access token in headers:

Authorization: Bearer <access_token>

📌 API Endpoints
🔹 Task APIs
Method	Endpoint	Description
POST	/api/tasks/         #	Create task
GET	/api/tasks/	          # List tasks
GET	/api/tasks/{id}/	    # Task detail
PATCH	/api/tasks/{id}/	  # Update task
DELETE	/api/tasks/{id}/	# Delete task

🔹 Filtering & Sorting
GET /api/tasks/?status=PENDING
GET /api/tasks/?priority=HIGH                 
GET /api/tasks/?ordering=due_date            
GET /api/tasks/?due_date__gte=2026-01-01      

🔹 Activity Logs
GET /api/activity-logs/


Tracks:

Task updates

Status changes

Task deletion

👥 User Roles:

INTERN

Can only view and manage their own tasks

ADMIN

Can view and manage all tasks

Permissions are enforced using DRF permission classes.

⏰ Overdue Task Automation

Runs automatically using Celery Beat

Checks for tasks where:

due_date < current_date AND status != COMPLETED


Updates status to OVERDUE

Logs the change in activity logs

🧪 API Testing

APIs were tested using:

Django REST Framework browsable API

Thunder Client (VS Code extension)
