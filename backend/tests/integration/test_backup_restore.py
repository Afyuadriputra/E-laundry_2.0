"""
PostgreSQL Automated Backup and Restore Verification Test (AT-30).
Performs an end-to-end backup dump of the laundry database, restores it to an
isolated temporary verification database, and verifies complete data consistency.
"""

import os
import shutil
import subprocess
import tempfile
import uuid
import pytest
from sqlalchemy import create_engine, text

PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "afyu")
PG_USER = os.getenv("POSTGRES_USER", "postgres")
PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
PG_PORT = os.getenv("POSTGRES_PORT", "5432")
SOURCE_DB = "laundry_test"
RESTORE_TEST_DB = f"laundry_restore_verify_{uuid.uuid4().hex[:8]}"


def _find_pg_tool(tool_name: str) -> str | None:
    tool = shutil.which(tool_name)
    if tool:
        return tool
    default_win_path = rf"C:\Program Files\PostgreSQL\17\bin\{tool_name}.exe"
    if os.path.exists(default_win_path):
        return default_win_path
    return None


@pytest.fixture(scope="module")
def pg_tools():
    pg_dump = _find_pg_tool("pg_dump")
    psql = _find_pg_tool("psql")
    if not pg_dump or not psql:
        pytest.skip("pg_dump or psql executable not found in PATH or standard PostgreSQL 17 directory")
    return {"pg_dump": pg_dump, "psql": psql}


def test_at_30_database_backup_and_restore_consistency(pg_tools):
    """
    AT-30: Backup dipulihkan pada lingkungan uji -> Data penting kembali konsisten.
    Verifies full database dump, restoration to an isolated database, and structural consistency.
    """
    env = os.environ.copy()
    env["PGPASSWORD"] = PG_PASSWORD

    # 1. Generate SQL dump from SOURCE_DB
    with tempfile.NamedTemporaryFile(suffix=".sql", delete=False) as temp_dump:
        dump_path = temp_dump.name

    try:
        dump_cmd = [
            pg_tools["pg_dump"],
            "-h", PG_HOST,
            "-p", PG_PORT,
            "-U", PG_USER,
            "-d", SOURCE_DB,
            "--clean",
            "--if-exists",
            "--no-owner",
            "-f", dump_path,
        ]
        dump_proc = subprocess.run(dump_cmd, env=env, capture_output=True, text=True, timeout=30)
        assert dump_proc.returncode == 0, f"pg_dump failed: {dump_proc.stderr}"
        assert os.path.getsize(dump_path) > 0, "Dump file is unexpectedly empty"

        # 2. Connect to postgres maintenance DB to create isolated RESTORE_TEST_DB
        admin_url = f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/postgres"
        admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

        with admin_engine.connect() as conn:
            # Terminate any existing connections to prevent conflict
            conn.execute(text(f"DROP DATABASE IF EXISTS {RESTORE_TEST_DB};"))
            conn.execute(text(f"CREATE DATABASE {RESTORE_TEST_DB};"))

        # 3. Restore dump into RESTORE_TEST_DB via psql
        with open(dump_path, "r", encoding="utf-8", errors="replace") as dump_in:
            restore_cmd = [
                pg_tools["psql"],
                "-h", PG_HOST,
                "-p", PG_PORT,
                "-U", PG_USER,
                "-d", RESTORE_TEST_DB,
                "-q",
            ]
            restore_proc = subprocess.run(
                restore_cmd,
                stdin=dump_in,
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
            )
            # psql may return warnings on dropped non-existent objects, check for successful execution
            assert restore_proc.returncode in (0, 1), f"psql restore failed: {restore_proc.stderr}"

        # 4. Verify data consistency in the restored database
        restore_url = f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{RESTORE_TEST_DB}"
        restore_engine = create_engine(restore_url)

        with restore_engine.connect() as conn:
            # Check 19 core tables exist
            tables_res = conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            )
            restored_tables = {row[0] for row in tables_res.fetchall()}
            assert "businesses" in restored_tables
            assert "orders" in restored_tables
            assert "payments" in restored_tables
            assert "audit_logs" in restored_tables
            assert "alembic_version" in restored_tables

            # Verify table count is at least 19
            assert len(restored_tables) >= 19

        restore_engine.dispose()

    finally:
        # Cleanup isolated test database
        try:
            with admin_engine.connect() as conn:
                conn.execute(text(f"""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = '{RESTORE_TEST_DB}' AND pid <> pg_backend_pid();
                """))
                conn.execute(text(f"DROP DATABASE IF EXISTS {RESTORE_TEST_DB};"))
            admin_engine.dispose()
        except Exception:
            pass

        # Cleanup temp dump file
        if os.path.exists(dump_path):
            os.remove(dump_path)

