
# Role-Based Access Control (RBAC) System

## Project Overview

This project is a Role-Based Access Control (RBAC)
application developed using Django REST Framework,
React.js, and PostgreSQL.

The system provides secure authentication,
role management, permission assignment,
employee management, and report generation.

## Technology Stack

### Backend
- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication

### Frontend
- React.js
- Vite
- JavaScript
- Axios

## Main Features

1. JWT-based Login and Logout
2. User Management
3. Role Management
4. Permission Assignment
5. Employee Management
6. Reports Generation and Download
7. User Settings
8. User Profile
9. Protected API Endpoints
10. Role-based Frontend Navigation

## User Roles

| Role | Access |
|---|---|
| Administrator | Full access |
| HR Manager | Employee management and HR reports |
| HR Executive | View and create employee records |
| Finance Manager | Financial reports |
| Employee | Personal dashboard and own profile |

## Project Structure

- accounts/ - Authentication and user management
- roles/ - Roles and permissions
- employees/ - Employee records
- reports/ - Report generation
- config/ - Django project configuration
- frontend/ - React application

## Backend Installation

1. Clone the repository.
2. Open the backend folder.
3. Create a virtual environment.
4. Activate the virtual environment.
5. Install dependencies.
6. Configure PostgreSQL.
7. Run migrations.
8. Start the Django server.

Commands:

```bash
python -m venv venv
```

Windows activation:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start backend:

```bash
python manage.py runserver
```

## Frontend Installation

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/auth/login/ | Login |
| POST | /api/auth/logout/ | Logout |
| GET | /api/auth/users/ | List users |
| GET | /api/roles/roles/ | List roles |
| GET | /api/employees/ | List employees |
| GET | /api/employees/me/ | Own profile |
| POST | /api/reports/generate/ | Generate report |
| GET | /api/reports/ | List reports |

## Security

- JWT authentication
- Password hashing
- Role-based API permissions
- Protected frontend routes
- Inactive user login prevention
- Employee profile privacy
- Prevention of unauthorized role changes

## Testing

Run all backend tests:

```bash
python manage.py test
```

## Developer

Hanna Jasmin

RBAC Machine Test Project
