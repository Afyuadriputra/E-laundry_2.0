import uuid

from sqlalchemy.orm import Session

from app.modules.audit.models import AuditLog
from app.modules.audit.service import AuditService, _redact_dict


def test_audit_sensitive_field_redaction():
    data = {
        "username": "kasir_budi",
        "password": "SecretPassword123!",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$xyz",
        "nested": {
            "session_token": "token_abc_123",
            "safe_field": "public_note",
        },
    }
    redacted = _redact_dict(data)
    assert redacted is not None
    assert redacted["username"] == "kasir_budi"
    assert redacted["password"] == "[REDACTED]"
    assert redacted["password_hash"] == "[REDACTED]"
    assert redacted["nested"]["session_token"] == "[REDACTED]"
    assert redacted["nested"]["safe_field"] == "public_note"


def test_audit_log_record_lifecycle(db_session: Session):
    order_id = uuid.uuid4()
    actor_id = uuid.uuid4()

    entry = AuditService.record(
        db=db_session,
        action="ORDER_CANCELLED",
        resource_type="order",
        actor_user_id=actor_id,
        resource_id=order_id,
        before_data={"status": "RECEIVED"},
        after_data={"status": "CANCELLED"},
        reason="Salah input tanggal",
    )
    db_session.commit()

    saved = db_session.query(AuditLog).filter(AuditLog.id == entry.id).first()
    assert saved is not None
    assert saved.action == "ORDER_CANCELLED"
    assert saved.resource_type == "order"
    assert saved.resource_id == order_id
    assert saved.reason == "Salah input tanggal"
    assert saved.created_at is not None
