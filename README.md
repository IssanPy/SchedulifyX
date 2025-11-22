# SchedulifyX

SchedulifyX is a lightweight appointment booking system aimed at clinics, coaches, salons and other service businesses. Built with Flask for rapid delivery and easy deployment. Includes simple service management, booking form, and a minimal admin interface to view/confirm appointments

## Features
- Service listing and service-based bookings.
- Booking form with date/time input.
- Simple appointment model with status (pending / confirmed / cancelled).
- Minimal admin CLI commands to seed data and create admin/creator users.
- Zero-config local DB using SQLite (easy to migrate to PostgreSQL).
- Mobile-responsive UI using Bootstrap.

## Tech stack
- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-WTF (forms & validation)
- Bootstrap 5 (frontend)
- SQLite (default, file-based DB)

## Quick start (local)
```bash
