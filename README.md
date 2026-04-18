# HelpDesk Pro — Django Chat-Based Helpdesk System

A full-featured, multi-page helpdesk system built with Django — white & navy blue theme.

---

## Project Structure

```
helpdesk_project/
│
├── manage.py
├── requirements.txt
├── seed_data.py
│
├── helpdesk/                  Main Django config app
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
│
├── accounts/                  Module A: User Management
│   ├── models.py              Custom User with Admin/Agent/User roles
│   ├── views.py               Login, Register, Profile, User list
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── tickets/                   Module B: Ticket Management
│   ├── models.py              Ticket + TicketComment
│   ├── views.py               CRUD + filtering by status/priority
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── knowledge/                 Module C: Knowledge Base
│   ├── models.py              Article + Category
│   ├── views.py               List, Detail, Create, Update, Delete
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── analytics/                 Module D: Analytics and Visualization
│   ├── views.py               Trend, status, priority charts + agent performance
│   └── urls.py
│
└── templates/
    ├── base.html              Sidebar layout (navy blue + white)
    ├── home.html              Public landing page
    ├── dashboard.html         Main dashboard with stats
    ├── accounts/
    │   ├── login.html
    │   ├── register.html
    │   ├── profile.html
    │   └── user_list.html
    ├── tickets/
    │   ├── ticket_list.html
    │   ├── ticket_detail.html
    │   └── ticket_form.html
    ├── knowledge/
    │   ├── article_list.html
    │   ├── article_detail.html
    │   └── article_form.html
    └── analytics/
        └── dashboard.html
```

---

## Setup Instructions

### Step 1 — Check Python and pip
```bash
python --version     # Must be 3.9 or higher
pip --version
```

### Step 2 — Navigate to the project folder
```bash
cd helpdesk_project
```

### Step 3 — Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac and Linux
python -m venv venv
source venv/bin/activate
```

### Step 4 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Run database migrations
```bash
python manage.py makemigrations accounts
python manage.py makemigrations tickets
python manage.py makemigrations knowledge
python manage.py makemigrations analytics
python manage.py migrate
```

### Step 6 — Load demo data (optional but recommended)
```bash
python seed_data.py
```

This creates the following demo accounts:

| Username  | Password | Role  |
|-----------|----------|-------|
| admin     | admin123 | Admin |
| agent1    | agent123 | Agent |
| john_doe  | user123  | User  |

It also creates sample tickets, comments, and knowledge base articles.

### Step 7 — Collect static files
```bash
python manage.py collectstatic --noinput
```

### Step 8 — Start the development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Role Permissions

| Feature                           | Admin | Agent | User |
|-----------------------------------|-------|-------|------|
| View own tickets                  | Yes   | Yes   | Yes  |
| Create tickets                    | Yes   | Yes   | Yes  |
| View all tickets                  | Yes   | Yes   | No   |
| Assign tickets to agents          | Yes   | Yes   | No   |
| Change ticket status              | Yes   | Yes   | No   |
| Delete tickets                    | Yes   | No    | No   |
| Create and edit Knowledge Base    | Yes   | Yes   | No   |
| View Analytics dashboard          | Yes   | Yes   | No   |
| Manage users                      | Yes   | No    | No   |
| Access Django Admin panel         | Yes   | No    | No   |

---

## URL Reference

| URL                       | Page                           |
|---------------------------|--------------------------------|
| /                         | Public landing page            |
| /accounts/login/          | Login                          |
| /accounts/register/       | Register                       |
| /accounts/profile/        | Edit profile                   |
| /accounts/users/          | User list (Admin only)         |
| /dashboard/               | Main dashboard with stats      |
| /tickets/                 | All tickets (filtered by role) |
| /tickets/create/          | Create new ticket              |
| /tickets/<id>/            | Ticket detail with comments    |
| /tickets/<id>/update/     | Edit ticket                    |
| /knowledge/               | Knowledge base article list    |
| /knowledge/create/        | New article (Agent and Admin)  |
| /knowledge/<id>/          | Article detail                 |
| /analytics/               | Analytics and charts           |
| /admin/                   | Django admin panel             |

---

## Technologies Used

| Layer    | Technology                         |
|----------|------------------------------------|
| Backend  | Django 4.2, Python 3.9+           |
| Database | SQLite (default), PostgreSQL ready |
| Frontend | Vanilla HTML, CSS, JavaScript      |
| Charts   | Chart.js 4.4 (CDN)                |
| Icons    | Font Awesome 6.5 (CDN)            |
| Fonts    | Plus Jakarta Sans (Google Fonts)   |
| Auth     | Django built-in session auth       |

---

## Production Checklist

Before going live, update helpdesk/settings.py:

```python
# Use a strong secret key from an environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')

# Disable debug mode
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# Switch to PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'helpdesk_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## How to Promote a User to Agent Role

1. Go to /admin/
2. Click Accounts > Users
3. Select the user you want to promote
4. Change the Role field to "agent"
5. Click Save

---

Built with Django — Navy Blue and White theme
