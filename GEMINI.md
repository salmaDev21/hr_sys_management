# Project: HR Management System (Absence Tracking)

This is a Django-based HR Management System focused on tracking employee absences and "reprise" (return-to-work) forms. It features a hierarchical organizational structure and role-based access control.

## Project Overview

- **Purpose:** Automate and track absence management and return-to-work procedures.
- **Key Modules:**
  - **Absence Forms:** Capture start/end dates, reasons, frequency, and impact analysis.
  - **Organizational Hierarchy:** Manage Departments (DPT), Units (UEP), Positions (Poste), and Employees (Collaborateur).
  - **Role-Based Access:** Tailored dashboards for Superadmins, HRBPs, and Managers (N+1).

## Technology Stack

- **Backend:** Python 3.12+, Django 6.0
- **Database:** SQLite (default `db.sqlite3`)
- **Frontend:** Tailwind CSS v4 (built with `@tailwindcss/cli`)
- **Templates:** Django Templates (organized by role in `templates/organization/`)

## Architecture & Data Model

### Organizational Hierarchy (4-tier)
1. **DPT (Department):** Managed by an HRBP.
2. **UEP (Unit):** Belongs to a DPT, managed by an NPLUS1 Manager.
3. **Poste (Position):** Belongs to a UEP.
4. **Collaborateur (Employee):** Assigned to a Poste.

### User Roles (`accounts.User`)
- `SUPERADMIN`: Full system access.
- `HRBP`: Access to their assigned Department (DPT).
- `NPLUS1`: Access to their assigned Unit (UEP) and subordinates.

### Core Logic (`organization.RepriseForm`)
- Tracks absence details (dates, type, reason).
- Monitors frequency (e.g., 2nd, 3rd, 4th+ absence).
- Records organizational impacts (recruitment, reorganization).
- Documents action plans (training, reassignment).

## Key Commands

### Development
- **Run Development Server:** `python manage.py runserver`
- **Tailwind CSS Watch:** `npm run watch:css` (compiles `static/src/style.css` to `static/dist/style.css`)
- **Database Migrations:** `python manage.py makemigrations` and `python manage.py migrate`
- **Create Superuser:** `python manage.py createsuperuser`

### Testing
- **Run Tests:** `python manage.py test` (Note: Tests currently need implementation in `accounts/tests.py` and `organization/tests.py`)

## Development Conventions

- **Authentication:** All views should be protected with `@login_required`.
- **Authorization:** Perform explicit role checks within views (e.g., `if request.user.role != 'HRBP': return redirect('forbidden')`).
- **Styling:** Use Tailwind CSS utility classes. Ensure the CSS build process is running during development.
- **Models:**
  - Use `corporate_id` as the primary unique identifier for users and employees where applicable.
  - Hierarchy is strictly enforced via ForeignKeys.
- **Templates:** Use role-specific subdirectories in `templates/organization/` for better organization.

## Directory Structure

- `/accounts`: Authentication, custom User model, and profiles.
- `/organization`: Core hierarchy, absence forms, and business logic.
- `/config`: Django project configuration and settings.
- `/static`: Assets and compiled CSS.
- `/templates`: HTML templates, grouped by role.
