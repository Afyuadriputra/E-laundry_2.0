#!/usr/bin/env bash
# ==============================================================================
# E-Laundry 2.0 - Automated PostgreSQL Restore Script
# TRD §3.5 & BSD §35: Point-In-Time Disaster Recovery
# ==============================================================================

set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <path_to_backup.sql.gz>"
    echo "Example: $0 ./backups/elaundry_backup_20261103_120000.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "[ERROR] Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

CONTAINER_NAME="${DB_CONTAINER:-elaundry-db-prod}"
DB_NAME="${POSTGRES_DB:-elaundry_db}"
DB_USER="${POSTGRES_USER:-elaundry_user}"

echo "====================================================================="
echo "WARNING: This operation will restore database '${DB_NAME}' from:"
echo "  ${BACKUP_FILE}"
echo "Existing data will be replaced per SQL dump commands."
echo "====================================================================="
read -p "Are you sure you want to proceed with restore? (yes/no): " CONFIRM
if [ "${CONFIRM}" != "yes" ]; then
    echo "[INFO] Restore aborted by operator."
    exit 0
fi

echo "[INFO] [$(date)] Starting restore..."

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "[INFO] Streaming decompressed SQL into container: ${CONTAINER_NAME}..."
    gunzip -c "${BACKUP_FILE}" | docker exec -i "${CONTAINER_NAME}" psql -U "${DB_USER}" -d "${DB_NAME}"
else
    echo "[INFO] Streaming decompressed SQL directly via host psql..."
    gunzip -c "${BACKUP_FILE}" | psql -U "${DB_USER}" -d "${DB_NAME}"
fi

echo "[SUCCESS] [$(date)] Database '${DB_NAME}' successfully restored from ${BACKUP_FILE}."

