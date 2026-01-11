Django Task Manager Backend API

Backend REST API built using Django and Django REST Framework with authentication, role-based access, filtering, activity logs, and background job processing using Celery + Redis.

🛠 Tech Stack

Python

Django

Django REST Framework

SimpleJWT (JWT Authentication)

django-filter

Celery

Redis

Docker (for Redis)

📁 Project Structure
'''
config/
│
├── config/                  # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── __init__.py
│
├── tasks/                   # Task management app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tasks_celery.py
│   ├── admin.py
│   └── migrations/
│
├── users/                   # User & role management app
│   ├── models.py
│   ├── admin.py
│   ├── views.py
│   └── migrations/
│
├── manage.py
├── README.md
└── venv/                    # Virtual environment 

'''
Setup Instructions:

1️⃣ Clone the Repository
'git clone <your-repository-url>'
'cd config'

2️⃣ Create & Activate Virtual Environment
'python -m venv venv'
'venv\Scripts\activate'   # Windows

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

▶️ Run the Application

Open three terminals:

Terminal 1 — Django Server
python manage.py runserver

Terminal 2 — Celery Worker
celery -A config worker -l info -P solo

Terminal 3 — Celery Beat (Scheduler)
python -m celery -A config beat -l info

🔐 Authentication

JWT Authentication using SimpleJWT

Access token required in request headers:

Authorization: Bearer <access_token>

📌 API Features

Task CRUD operations

Role-based access:

ADMIN → full access

INTERN → only own tasks

Filtering, sorting & pagination

Activity logging for updates, status changes & deletion

Automated overdue task handling via Celery

⏰ Background Job (Overdue Tasks)

Runs on a schedule using Celery Beat

Finds tasks past due_date

Marks them as OVERDUE

Creates activity log entry

