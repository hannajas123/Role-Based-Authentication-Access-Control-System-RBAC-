# Role-Based Access Control (RBAC) System

A secure, enterprise-grade Role-Based Access Control (RBAC) web application developed with **Python Django REST Framework**, **React.js**, and **PostgreSQL**.

The system enables granular access control where users authenticate via JWT and access application modules, actions, and reports strictly according to their assigned roles and permissions.

---

## 1. Mandatory Test Login Credentials

The application includes pre-configured demo accounts for all five required roles. You can provision or reset all roles, permissions, demo users, and sample data using a single management command:

```bash
python manage.py seed_rbac
```

| Role | Username | Email | Password | Access Scope & Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin@example.com` | `Admin@12345` | **Full System Access:** User management, role creation, permission matrix assignment, employee records, reports, system settings. |
| **HR Manager** | `hr_manager` | `hrmanager@example.com` | `HRManager@12345` | **HR Management:** Access HR Dashboard, full CRUD on Employee records (`View`, `Create`, `Edit`, `Delete`), view/generate/download Employee HR reports. |
| **HR Executive** | `hr_exec` | `hrexec@example.com` | `HRExec@12345` | **HR Operations:** View and Create employee records only. *Cannot edit or delete employee records.* |
| **Finance Manager** | `finance_mgr` | `finance@example.com` | `Finance@12345` | **Finance Operations:** Access Finance Dashboard, view/generate/download Financial reports and CSV statements. |
| **Employee** | `employee_user` | `employee@example.com` | `Employee@12345` | **Self-Service:** Access Personal Dashboard, view own employee profile (`/api/employees/me/`). Private records of other employees are strictly isolated. |

> **Note:** Users can log in using either their **Username** or their **Email address**.

---

## 2. Technology Stack

- **Backend:** Python 3.11+, Django 5.2, Django REST Framework (DRF)
- **Frontend:** React.js (v19), Vite, React Router DOM (v7), Axios
- **Database:** PostgreSQL (Preferred)
- **Authentication:** JSON Web Tokens (SimpleJWT) with access token rotation and refresh token blacklisting
- **Security:** PBKDF2 password hashing, backend permission enforcement (`HasModulePermission`), frontend route guards

---

## 3. RBAC Architecture & Module Permissions

The RBAC system defines predefined permissions grouped by module:

| Module | Available Permissions |
| :--- | :--- |
| **Dashboard** | `View` |
| **User Management** | `View`, `Create`, `Edit`, `Delete` |
| **Role Management** | `View`, `Create`, `Edit`, `Delete` |
| **Employee Management** | `View`, `Create`, `Edit`, `Delete` |
| **Reports** | `View`, `Generate`, `Download` |
| **Settings** | `View`, `Edit` |

### Role-Permission Matrix

| Permission | Administrator | HR Manager | HR Executive | Finance Manager | Employee |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Dashboard: View** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **User Management (All CRUD)** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Role Management (All CRUD)** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Employee Management: View** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Employee Management: Create** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Employee Management: Edit** | ✅ | ✅ | ❌ *(Forbidden)* | ❌ | ❌ |
| **Employee Management: Delete** | ✅ | ✅ | ❌ *(Forbidden)* | ❌ | ❌ |
| **Reports: View** | ✅ | ✅ *(HR only)* | ❌ | ✅ *(Finance only)*| ❌ |
| **Reports: Generate** | ✅ | ✅ *(HR only)* | ❌ | ✅ *(Finance only)*| ❌ |
| **Reports: Download** | ✅ | ✅ *(HR only)* | ❌ | ✅ *(Finance only)*| ❌ |
| **Settings: View / Edit** | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 4. Frontend Application Pages (React.js)

The application provides the 9 pages requested by the specification, with route-level security guards:

1. **Login Page (`/login`):** Dual username/email authentication with JWT handling.
2. **Dashboard (`/dashboard`):** Role-tailored dashboards:
   - *Admin Dashboard:* System statistics (Users, Roles, Employees, Reports), security status checklist, quick admin links.
   - *HR Manager Dashboard:* Employee directory stats, HR reports overview, shortcuts to add employee and run HR reports.
   - *HR Executive Dashboard:* Directory overview with strict notice highlighting view/create privileges.
   - *Finance Manager Dashboard:* Financial report overview and statement generation shortcuts.
   - *Employee Personal Dashboard:* Employee profile snapshot (Department, Designation, Joining date) and permitted permissions list.
3. **User Management (`/users`):** Admin-only CRUD for system users, role assignment, and active/inactive status toggling.
4. **Role Management (`/roles`):** Admin-only creation and editing of roles and assigned permissions. Administrator role is protected against modification and deletion.
5. **Permission Management (`/permissions`):** Interactive matrix view enabling Administrators to inspect and toggle permissions across roles in real-time.
6. **Employee Management (`/employees`):** Employee record management with button-level and API-level permission enforcement (HR Executive cannot edit or delete).
7. **Reports (`/reports`):** Role-isolated report management: HR Managers generate/download Employee reports; Finance Managers generate/download Financial reports; CSV export functionality.
8. **Settings (`/settings`):** Account-level preferences (email notifications, theme selection).
9. **User Profile (`/profile`):** Personal account and employee record details (`/api/employees/me/`).

### Frontend Security Features:
- **Direct URL Protection:** Unauthorized URL navigation triggers a dedicated **403 - Access Denied** screen.
- **Dynamic Menus:** The sidebar navigation displays only the modules the authenticated user has permissions to view.
- **Action Hiding:** Create, Edit, Delete, Generate, and Download buttons are hidden if the user's role lacks that specific action.
- **Session Persistence:** Authenticated sessions persist on browser refresh.

---

## 5. Installation & Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL running locally on port 5432 (or configured in `config/settings.py`)

### 1. Database Configuration
Create a PostgreSQL database named `rbac_db`:
```sql
CREATE DATABASE rbac_db;
```
Verify the credentials in `config/settings.py` (Default: `USER: postgres`, `PASSWORD: hannaja123`, `PORT: 5432`, `NAME: rbac_db`).

### 2. Backend Setup
In a terminal, navigate to the project root directory:

```bash
# 1. Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# (Or Linux/macOS: source venv/bin/activate)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Seed all roles, permissions, demo users, and initial reports
python manage.py seed_rbac

# 5. Start the Django development server
python manage.py runserver
```
The backend API will be available at: `http://127.0.0.1:8000/`

### 3. Frontend Setup
In a separate terminal, navigate to the `frontend` folder:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
The React frontend will be available at: `http://localhost:5173/`

---

## 6. API Documentation

| Method | Endpoint | Module | Action | Access Rule | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login/` | - | - | Public | Login via username or email; returns JWT access and refresh tokens. |
| `POST` | `/api/auth/logout/` | - | - | Authenticated | Logout; blacklists the provided refresh token. |
| `GET` | `/api/auth/users/` | User Management | View | Administrator Only | List all registered user accounts. |
| `POST` | `/api/auth/users/` | User Management | Create | Administrator Only | Create user with username, email, password, and role. |
| `PATCH` | `/api/auth/users/<id>/` | User Management | Edit | Administrator Only | Update user, activate/deactivate user, or change role. Self-role elevation is blocked. |
| `DELETE` | `/api/auth/users/<id>/` | User Management | Delete | Administrator Only | Delete user account. |
| `GET` | `/api/roles/roles/` | Role Management | View | Administrator Only | List all available roles with assigned permissions. |
| `POST` | `/api/roles/roles/` | Role Management | Create | Administrator Only | Create custom role with permissions. |
| `PATCH` | `/api/roles/roles/<id>/` | Role Management | Edit | Administrator Only | Update role description or permissions. Administrator role is protected. |
| `DELETE` | `/api/roles/roles/<id>/` | Role Management | Delete | Administrator Only | Delete role. Cannot delete Administrator or roles assigned to users. |
| `GET` | `/api/roles/permissions/` | Role Management | View | Authenticated | List all predefined system permissions. |
| `GET` | `/api/employees/` | Employee Management | View | Admin, HR Manager, HR Exec | List all employee records. |
| `POST` | `/api/employees/` | Employee Management | Create | Admin, HR Manager, HR Exec | Create employee profile and user record. |
| `PATCH` | `/api/employees/<id>/` | Employee Management | Edit | Admin, HR Manager | Update employee record. **HR Executive is blocked (403).** |
| `DELETE` | `/api/employees/<id>/` | Employee Management | Delete | Admin, HR Manager | Delete employee record. **HR Executive is blocked (403).** |
| `GET` | `/api/employees/me/` | - | - | Authenticated | View authenticated user's own employee profile. |
| `GET` | `/api/reports/` | Reports | View | Admin, HR Manager, Finance Mgr | List reports. Isolated by role (HR = employee reports; Finance = financial reports). |
| `POST` | `/api/reports/generate/` | Reports | Generate | Admin, HR Manager, Finance Mgr | Generate report. Validates allowed report type by role. |
| `GET` | `/api/reports/<id>/download/` | Reports | Download | Admin, HR Manager, Finance Mgr | Download report as CSV. |
| `GET` | `/api/auth/settings/` | Settings | View | Admin, Permitted roles | View account settings. |
| `PATCH` | `/api/auth/settings/` | Settings | Edit | Admin, Permitted roles | Update theme and notification preferences. |

---

## 7. Automated Test Suite & Scenario Verification

The project includes **26 comprehensive automated test cases** that validate all 10 critical test scenarios specified by the machine test requirements.

### Running Backend Tests:
```bash
python manage.py test
```

### Test Scenario Coverage Matrix:

| Scenario # | Required Test Scenario | Test Implementation | Result |
| :---: | :--- | :--- | :---: |
| **1** | Administrator can access all modules | `roles/tests.py`, `employees/tests.py`, `reports/tests.py` | ✅ Passed |
| **2** | Each role can access only its permitted modules | `employees/tests.py`, `reports/tests.py` | ✅ Passed |
| **3** | Users cannot access unauthorized pages or APIs | `accounts/tests.py`, `roles/tests.py`, `reports/tests.py` | ✅ Passed |
| **4** | HR Executive cannot edit or delete employee records | `EmployeeSecurityAndRBACTests.test_hr_executive_cannot_edit_employee_records` & `test_hr_executive_cannot_delete_employee_records` | ✅ Passed |
| **5** | Employees cannot view other employees' private information | `EmployeeSecurityAndRBACTests.test_employee_cannot_view_all_employees` & `test_employee_cannot_view_specific_other_employee` | ✅ Passed |
| **6** | Administrator can create users and assign roles | `AuthenticationAndUserSecurityTests.test_admin_can_create_user_and_assign_role` | ✅ Passed |
| **7** | Administrator can create roles and assign permissions | `RoleAndPermissionTests.test_admin_can_create_role_and_assign_permissions` | ✅ Passed |
| **8** | Changes in roles and permissions are reflected in user access | `RoleAndPermissionTests.test_changes_in_role_permissions_reflected_immediately` | ✅ Passed |
| **9** | Deactivated users cannot access the application | `AuthenticationAndUserSecurityTests.test_deactivated_user_cannot_login` | ✅ Passed |
| **10** | Users cannot increase their own permissions or privileges | `AuthenticationAndUserSecurityTests.test_user_cannot_elevate_own_role` | ✅ Passed |

---

## 8. Security Highlights

1. **Backend-Enforced Authorization:** Direct API calls via Postman or curl cannot bypass access restrictions; views validate permission via `HasModulePermission` and custom permission checks.
2. **Dual-Layer Protection:** The frontend hides unauthorized navigation and action buttons, while route guards display 403 pages on direct URL navigation.
3. **Privilege Escalation Prevention:** Users cannot modify their own roles or assign themselves elevated privileges.
4. **Token Security:** JWT access tokens have a 30-minute lifespan with refresh token rotation and explicit blacklisting on logout.
5. **Data Isolation:** Regular employees only have access to their personal profile endpoint (`/api/employees/me/`).
