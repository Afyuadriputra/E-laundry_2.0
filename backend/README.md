# Laundry UMKM Backend

Backend for Laundry UMKM Management System.

## Architecture

- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- Modular Monolith
- Router / Service / Domain / Repository

## Main Modules

- Authentication and Users
- Businesses and Settings
- Services
- Customers
- Orders
- Payments
- Expenses
- Pickup and Delivery
- Invoices
- Public Tracking
- Dashboard and Reports
- Audit and Idempotency

## Project Status

Architecture scaffold only.

Application logic, API endpoints, database migrations,
and test implementations have not been created yet.

## Important

- Never commit .env files.
- Never commit credentials.
- Database schema must be managed using Alembic.
- Business rules must follow PRD, TRD, AFD, DBD, BSD, and IPD.