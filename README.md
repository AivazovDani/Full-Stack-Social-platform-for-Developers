# DevSearch - Developer Social Platform

A full stack web application built with Django that allows developers to showcase their projects, connect with other developers, and receive feedback on their work.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Database](#database)
- [API](#api)
- [Usage](#usage)
- [Contributing](#contributing)

---

## Overview

DevSearch is a developer portfolio and social platform where developers can:

- Create and manage their developer profile
- Showcase their projects with images, tags, and links
- Receive upvote/downvote feedback on projects
- Search for projects and developers
- Send and receive messages to/from other developers
- Manage their skills

---

## Features

### Authentication
- User registration with custom form
- Login and logout
- Login required protection on sensitive pages
- JWT token support for API access
- Automatic profile creation via Django signals on registration

### Profiles
- View all developer profiles
- Single developer profile page
- Edit profile (name, bio, profile image, social links)
- Social links: GitHub, Twitter, LinkedIn, YouTube, Website
- Profile automatically synced with Django User model via signals

### Projects
- Create, read, update, delete projects
- Featured image upload
- Tags (ManyToMany relationship)
- Demo link and source code link
- Search projects by title, description, owner name, or tags
- Pagination with custom range display
- Only project owner can edit or delete their project

### Reviews
- Upvote or downvote projects
- Leave written feedback
- One review per user per project
- Users cannot review their own projects
- Must be logged in to leave a review
- Vote ratio and total votes automatically calculated

### Skills
- Add and delete skills on your profile
- Each skill has a name and description

### Messaging
- Send messages to other developers
- Inbox to view received messages
- Mark messages as read when opened
- Unread message count
- Anonymous messaging supported (name and email fields)

### Search & Pagination
- Search projects by title, description, owner, or tags
- Search developers by name, skills, or location
- Paginated results with custom page range
- Search query preserved across pages

### REST API
- API endpoints for projects and tags
- JWT authentication via SimpleJWT
- Remove tag from project via DELETE request
- CORS configured for frontend access

---

## Tech Stack

**Backend**
- Python 3.13
- Django 6.0
- Django REST Framework
- SimpleJWT (JWT Authentication)
- django-cors-headers

**Database**
- SQLite (development)
- PostgreSQL (recommended for production)

**Frontend**
- Django Templates
- HTML / CSS
- JavaScript (Fetch API for tag removal)
- Custom UIKit CSS framework

**Other**
- Pillow (image uploads)
- UUID primary keys for security
- Django Signals for automation

---

## Project Structure

```
devtest/
│
├── devtest/                  # Main project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── projects/                 # Projects app
│   ├── models.py             # Project, Review, Tag models
│   ├── views.py              # CRUD views + API views
│   ├── urls.py
│   ├── form.py               # ProjectForm, ReviewForm
│   ├── utils.py              # Search and pagination helpers
│   ├── serializers.py        # DRF serializers
│   └── templates/
│       └── projects/
│           ├── projects.html
│           ├── single-project.html
│           ├── project_form.html
│           └── delete_object.html
│
├── users/                    # Users app
│   ├── models.py             # Profile, Skill, Message models
│   ├── views.py              # Auth, profile, inbox views
│   ├── urls.py
│   ├── form.py               # ProfileForm, MessageForm, CustomUserCreationForm
│   ├── signals.py            # Auto create/update profile
│   ├── apps.py               # Loads signals on startup
│   └── templates/
│       └── users/
│           ├── profiles.html
│           ├── user-profile.html
│           ├── login_register.html
│           ├── account.html
│           └── inbox.html
│
├── templates/                # Shared templates
│   ├── main.html
│   ├── navbar.html
│   └── pagination.html
│
├── static/                   # Static files
│   ├── style/
│   └── uikit/
│
├── manage.py
└── db.sqlite3
```

---

## Installation

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/devsearch.git
cd devsearch
```

**2. Create and activate virtual environment:**
```bash
python -m venv env
source env/bin/activate        # Mac/Linux
env\Scripts\activate           # Windows
```

**3. Install dependencies:**
```bash
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install djangorestframework-simplejwt
pip install Pillow
```

**4. Apply migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Create superuser:**
```bash
python manage.py createsuperuser
```

**6. Run the server:**
```bash
python manage.py runserver
```

---

## Environment Setup

Add the following to your `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'projects.apps.ProjectsConfig',
    'users.apps.UsersConfig',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # must be first
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

CORS_ALLOW_ALL_ORIGINS = True  # development only

LOGIN_URL = 'loginPage'

MEDIA_URL = '/images/'
MEDIA_ROOT = BASE_DIR / 'static/images'
```

---

## Database

### Models

**Profile**
```
user          OneToOneField → User
name          CharField
username      CharField
email         EmailField
short_intro   CharField
bio           TextField
profile       ImageField
social_github CharField
social_twitter CharField
social_linkedin CharField
social_youtube CharField
social_website CharField
id            UUIDField (primary key)
```

**Project**
```
owner         ForeignKey → Profile
title         CharField
description   TextField
featured_image ImageField
demo_link     CharField
source_link   CharField
tags          ManyToManyField → Tag
vote_total    IntegerField
vote_ratio    IntegerField
id            UUIDField (primary key)
```

**Review**
```
owner         ForeignKey → Profile
project       ForeignKey → Project (related_name='reviews')
body          TextField
value         CharField (up/down)
id            UUIDField (primary key)
unique_together: [owner, project]
```

**Skill**
```
owner         ForeignKey → Profile
name          CharField
description   TextField
id            UUIDField (primary key)
```

**Message**
```
sender        ForeignKey → Profile (null=True)
recipient     ForeignKey → Profile (related_name='messages')
name          CharField
email         EmailField
subject       CharField
body          TextField
is_read       BooleanField (default=False)
id            UUIDField (primary key)
```

### Signals

Two signals keep the User and Profile models in sync:

- When a **User is created** → automatically create a **Profile**
- When a **Profile is updated** → automatically update the **User** (email, name, username)

---

## API

### Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/projects/` | List all projects |
| GET | `/api/projects/<id>/` | Get single project |
| DELETE | `/api/remove-tag/` | Remove tag from project |
| POST | `/api/token/` | Get JWT access token |
| POST | `/api/token/refresh/` | Refresh JWT token |

### Authentication

Generate a token:
```
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

Use the token in requests:
```
Authorization: Bearer <access_token>
```

---

## Usage

### Creating a Project
1. Log in to your account
2. Click "Add Project" in the navbar
3. Fill in title, description, image, links and tags
4. Submit — project is linked to your profile automatically

### Reviewing a Project
1. Visit any project page
2. If you are not the owner and haven't reviewed yet
3. Select upvote or downvote and leave a comment
4. Vote ratio updates automatically

### Sending a Message
1. Visit another developer's profile
2. Click "Send Message"
3. Fill in the form and submit
4. Message appears in the recipient's inbox

### Removing a Tag
Tags can be removed from your project edit page by clicking the tag — this fires a DELETE request to the API without reloading the page.

---

## Key Concepts

### Why UUID Primary Keys?
```
Sequential IDs (1, 2, 3) are predictable
→ users could guess other profile/project URLs

UUIDs are random and impossible to guess
→ more secure for public facing URLs
```

### Why Signals?
```
Signals automate reactions between models
User created → Profile auto created
Profile updated → User auto updated
No manual handling needed in views
```

### Why distinct() in Search?
```
A project with 3 matching tags
→ without distinct() appears 3 times
→ with distinct() appears only once
```

---

## Recommended Next Steps

- Switch from SQLite to PostgreSQL for production
- Deploy to Railway or Render
- Set DEBUG=False in production
- Configure proper ALLOWED_HOSTS
- Set up proper media file storage (AWS S3)
- Add email verification on registration
- Add password reset functionality
- Build a React frontend consuming the REST API

---

## License

MIT License — feel free to use this project for learning and portfolio purposes.
