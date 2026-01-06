# ERP Project (Python)

A simple **Employee Resource Planning (ERP)** system built with **FastAPI**, **SQLAlchemy**, **MySQL**, and **Alembic** for migrations.  
This project includes **user management**, **leave tracking**, and **role-based access** (admin/user).  

---

## Features

- Add, view, and manage users  
- Track employee leaves with status (`pending`, `approved`, `rejected`)  
- Admin and regular user roles  
- Database migrations using Alembic  
- RESTful API with **Swagger UI** for testing  

---

## Tech Stack

- **Backend:** Python 3.13, FastAPI  
- **Database:** MySQL  
- **ORM:** SQLAlchemy  
- **Migrations:** Alembic  
- **Environment Variables:** python-dotenv  
- **Password Security:** Passlib (bcrypt)  
- **JWT Authentication:** Python-JOSE (if implemented)  

---

## Project Structure

ERP_PROJECT_PYTHON/
│
├─ alembic/ # Alembic migrations
│ ├─ versions/ # Migration files
│ └─ env.py # Alembic env configuration
│
├─ models.py # SQLAlchemy ORM models
├─ database.py # Database connection and Base
├─ main.py # FastAPI application entry point
├─ routers/ # API routers (users, leaves)
├─ .env # Environment variables (DB credentials)
└─ requirements.txt # Python dependencies