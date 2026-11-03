-- E-Laundry 2.0 Local PostgreSQL Initialization Script
-- Sesuai dengan spesifikasi doc/TRD.md dan doc/BSD.md
-- Jalankan menggunakan user administratif PostgreSQL (postgres):
-- psql -U postgres -h localhost -f setup_postgres.sql

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'laundry_app') THEN
      CREATE ROLE laundry_app LOGIN PASSWORD 'laundry_dev_secret';
   END IF;
END
$do$;

SELECT 'CREATE DATABASE laundry_dev OWNER laundry_app'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'laundry_dev')\gexec

GRANT ALL PRIVILEGES ON DATABASE laundry_dev TO laundry_app;

\connect laundry_dev

GRANT ALL ON SCHEMA public TO laundry_app;
ALTER SCHEMA public OWNER TO laundry_app;
