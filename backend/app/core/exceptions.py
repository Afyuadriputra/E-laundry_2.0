from typing import Any


class AppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: list[dict[str, Any]] | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


class ValidationException(AppException):
    def __init__(
        self,
        message: str = "Input tidak valid",
        details: list[dict[str, Any]] | None = None,
    ):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=422,
            details=details,
        )


class UnauthenticatedException(AppException):
    def __init__(self, message: str = "Sesi tidak valid atau telah berakhir"):
        super().__init__(
            code="UNAUTHENTICATED",
            message=message,
            status_code=401,
        )


class ForbiddenException(AppException):
    def __init__(self, message: str = "Tidak memiliki izin untuk tindakan ini"):
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=403,
        )


class NotFoundException(AppException):
    def __init__(self, message: str = "Data tidak ditemukan"):
        super().__init__(
            code="RESOURCE_NOT_FOUND",
            message=message,
            status_code=404,
        )


class GoneException(AppException):
    def __init__(self, message: str = "Tautan atau sumber daya telah berakhir atau dicabut"):
        super().__init__(
            code="RESOURCE_GONE",
            message=message,
            status_code=410,
        )


class ConflictException(AppException):
    def __init__(self, code: str = "CONFLICT", message: str = "Konflik data"):
        super().__init__(
            code=code,
            message=message,
            status_code=409,
        )


class BusinessInvariantException(AppException):
    def __init__(self, message: str = "Pelanggaran aturan bisnis sistem"):
        super().__init__(
            code="BUSINESS_INVARIANT_VIOLATION",
            message=message,
            status_code=422,
        )


class ServiceUnavailableException(AppException):
    def __init__(self, message: str = "Dependency atau layanan tidak tersedia"):
        super().__init__(
            code="SERVICE_UNAVAILABLE",
            message=message,
            status_code=503,
        )
