import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.modules.audit.models import AuditLog

# Sensitive keys that must be strictly redacted per BSD.md Section 25.3 Rules 2 & 3
SENSITIVE_KEYS = {
    "password",
    "password_hash",
    "csrf_secret",
    "csrf_secret_hash_or_reference",
    "session_token",
    "session_token_hash",
    "raw_token",
    "token_hash",
}


def _redact_dict(data: dict[str, Any] | None) -> dict[str, Any] | None:
    if not data or not isinstance(data, dict):
        return data

    sanitized: dict[str, Any] = {}
    for k, v in data.items():
        if k.lower() in SENSITIVE_KEYS:
            sanitized[k] = "[REDACTED]"
        elif isinstance(v, dict):
            sanitized[k] = _redact_dict(v)
        else:
            sanitized[k] = v
    return sanitized


class AuditService:
    @staticmethod
    def record(
        db: Session,
        action: str,
        resource_type: str,
        actor_user_id: uuid.UUID | None = None,
        resource_id: uuid.UUID | None = None,
        request_id: str | None = None,
        before_data: dict[str, Any] | None = None,
        after_data: dict[str, Any] | None = None,
        reason: str | None = None,
    ) -> AuditLog:
        """
        Record a critical audit log event in accordance with BSD.md §25.
        Guarantees redaction of sensitive credentials.
        """
        log_entry = AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            request_id=request_id,
            before_data=_redact_dict(before_data),
            after_data=_redact_dict(after_data),
            reason=reason,
        )
        db.add(log_entry)
        db.flush()
        return log_entry
