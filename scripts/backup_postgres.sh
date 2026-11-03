#!/usr/bin/env bash
# ==============================================================================
# E-Laundry 2.0 - Automated PostgreSQL Backup Script
# TRD §3.5 & BSD §35: Production Disaster Recovery
# ==============================================================================

set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/elaundry_backup_${TIMESTAMP}.sql.gz"
RETENTION_DAYS="${RETENTION_DAYS:-14}"

# Database credentials (default from environment or Docker container)
CONTAINER_NAME="${DB_CONTAINER:-elaundry-db-prod}"
DB_NAME="${POSTGRES_DB:-elaundry_db}"
DB_USER="${POSTGRES_USER:-elaundry_user}"

mkdir -p "${BACKUP_DIR}"

echo "[INFO] [$(date)] Starting PostgreSQL backup for database: ${DB_NAME}..."

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "[INFO] Performing pg_dump via Docker container: ${CONTAINER_NAME}..."
    docker exec -t "${CONTAINER_NAME}" pg_dump -U "${DB_USER}" -d "${DB_NAME}" --clean --if-exists --no-owner | gzip > "${BACKUP_FILE}"
else
    echo "[INFO] Performing pg_dump directly via host..."
    pg_dump -U "${DB_USER}" -d "${DB_NAME}" --clean --if-exists --no-owner | gzip > "${BACKUP_FILE}"
fi

FILE_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
echo "[SUCCESS] [$(date)] Backup completed: ${BACKUP_FILE} (Size: ${FILE_SIZE})"

# Retention cleanup: remove backups older than RETENTION_DAYS
echo "[INFO] Cleaning up backups older than ${RETENTION_DAYS} days in ${BACKUP_DIR}..."
find "${BACKUP_DIR}" -type f -name "elaundry_backup_*.sql.gz" -mtime +"${RETENTION_DAYS}" -exec rm -f {} +

echo "[SUCCESS] Backup workflow finished successfully."

