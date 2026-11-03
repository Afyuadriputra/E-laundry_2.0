from app.core.security import hash_password, verify_password


def test_argon2_hashing_and_verification():
    raw_password = "SuperSecretPassword123!"
    hashed = hash_password(raw_password)

    assert hashed.startswith("$argon2id$")
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False
    assert verify_password("", hashed) is False


def test_argon2_unique_salts():
    raw_password = "CommonPassword456"
    hash_1 = hash_password(raw_password)
    hash_2 = hash_password(raw_password)

    # Hashes must differ due to cryptographic random salts
    assert hash_1 != hash_2
    assert verify_password(raw_password, hash_1) is True
    assert verify_password(raw_password, hash_2) is True
