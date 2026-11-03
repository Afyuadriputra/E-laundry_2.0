import hashlib
import hmac
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Argon2id password hasher with RFC 9106 recommended parameters
_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,  # 64 MB
    parallelism=2,
    hash_len=32,
    salt_len=16,
)


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using Argon2id."""
    return _hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an Argon2id hash."""
    try:
        return _hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, Exception):
        return False


def generate_session_token() -> str:
    """Generate a high-entropy random URL-safe session token (32 bytes = 256 bits)."""
    return secrets.token_urlsafe(32)


def hash_session_token(raw_token: str) -> str:
    """Generate SHA-256 hex digest of the raw session token for database lookup."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def generate_csrf_token() -> str:
    """Generate a high-entropy random URL-safe CSRF token."""
    return secrets.token_urlsafe(32)


def verify_csrf_token(received_token: str, expected_token: str) -> bool:
    """Perform constant-time comparison of CSRF tokens to prevent timing attacks."""
    if not received_token or not expected_token:
        return False
    return hmac.compare_digest(received_token, expected_token)
