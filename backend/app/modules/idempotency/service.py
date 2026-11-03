import hashlib
import json
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException
from app.modules.idempotency.models import IdempotencyRecord


class IdempotencyService:
    @staticmethod
    def _hash_string(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def _hash_payload(payload: Any) -> str:
        if isinstance(payload, str):
            serialized = payload
        else:
            try:
                serialized = json.dumps(payload, sort_keys=True, default=str)
            except Exception:
                serialized = str(payload)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    @classmethod
    def acquire(
        cls,
        db: Session,
        scope_key: str,
        operation: str,
        idempotency_key: str,
        payload: Any,
        ttl_minutes: int = 60,
    ) -> tuple[IdempotencyRecord | None, bool]:
        """Acquires or inspects an idempotency record.

        Returns (record, is_fresh_execution).
        If an identical request has already COMPLETED, returns (record, False).
        If the record exists with a DIFFERENT payload, raises ConflictException.
        If the record is currently PROCESSING, raises ConflictException.
        """
        key_hash = cls._hash_string(idempotency_key)
        request_hash = cls._hash_payload(payload)

        existing = (
            db.query(IdempotencyRecord)
            .filter(
                IdempotencyRecord.scope_key == scope_key,
                IdempotencyRecord.operation == operation,
                IdempotencyRecord.idempotency_key_hash == key_hash,
            )
            .first()
        )

        now = datetime.now(UTC)

        if existing:
            # Check if expired
            expires_at = existing.expires_at
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=UTC)
            if expires_at < now:
                db.delete(existing)
                db.flush()
            elif existing.request_hash != request_hash:
                raise ConflictException(
                    code="IDEMPOTENCY_PAYLOAD_MISMATCH",
                    message="Permintaan dengan Idempotency-Key yang sama memiliki payload yang berbeda.",
                )
            elif existing.status == "COMPLETED":
                return existing, False
            elif existing.status == "PROCESSING":
                raise ConflictException(
                    code="CONCURRENT_REQUEST_IN_FLIGHT",
                    message="Permintaan sedang diproses dalam transaksi lain. Mohon tunggu.",
                )

        # Create new processing record
        record = IdempotencyRecord(
            id=uuid.uuid4(),
            scope_key=scope_key,
            operation=operation,
            idempotency_key_hash=key_hash,
            request_hash=request_hash,
            status="PROCESSING",
            created_at=now,
            expires_at=now + timedelta(minutes=ttl_minutes),
        )
        db.add(record)
        db.flush()
        return record, True

    @classmethod
    def complete(
        cls,
        db: Session,
        record_id: uuid.UUID,
        status_code: int,
        response_body: str,
    ) -> None:
        record = db.query(IdempotencyRecord).filter(IdempotencyRecord.id == record_id).first()
        if record:
            record.status = "COMPLETED"
            record.response_status_code = status_code
            record.response_reference = response_body
            db.flush()

    @classmethod
    def fail(cls, db: Session, record_id: uuid.UUID) -> None:
        record = db.query(IdempotencyRecord).filter(IdempotencyRecord.id == record_id).first()
        if record:
            record.status = "FAILED"
            db.flush()
