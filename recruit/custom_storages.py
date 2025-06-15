"""Custom storage backends for static and media files using Amazon S3."""

from typing import Any

from django.conf import settings
from django.core.files.storage import DefaultStorage

try:
    from storages.backends.s3boto3 import S3Boto3Storage  # type: ignore[import-untyped]
except ImportError:
    # Fallback for older versions
    try:
        from storages.backends.s3boto import (  # type: ignore[import-untyped]
            S3BotoStorage as S3Boto3Storage
        )
    except ImportError:
        # Final fallback
        S3Boto3Storage = DefaultStorage  # type: ignore[assignment, misc]


class StaticStorage(S3Boto3Storage):  # type: ignore[misc]
    """Custom storage backend for static files using S3."""

    location = settings.STATICFILES_LOCATION

    def get_accessed_time(self, _name: str) -> Any:
        """Raise NotImplementedError as this backend doesn't support accessed time."""
        raise NotImplementedError("This backend doesn't support accessed time.")

    def get_created_time(self, _name: str) -> Any:
        """Raise NotImplementedError as this backend doesn't support created time."""
        raise NotImplementedError("This backend doesn't support created time.")

    def path(self, _name: str) -> str:
        """Raise NotImplementedError as this backend doesn't support local paths."""
        raise NotImplementedError("This backend doesn't support local file paths.")


class MediaStorage(S3Boto3Storage):  # type: ignore[misc]
    """Custom storage backend for media files using S3."""

    location = settings.MEDIAFILES_LOCATION

    def get_accessed_time(self, _name: str) -> Any:
        """Raise NotImplementedError as this backend doesn't support accessed time."""
        raise NotImplementedError("This backend doesn't support accessed time.")

    def get_created_time(self, _name: str) -> Any:
        """Raise NotImplementedError as this backend doesn't support created time."""
        raise NotImplementedError("This backend doesn't support created time.")

    def path(self, _name: str) -> str:
        """Raise NotImplementedError as this backend doesn't support local paths."""
        raise NotImplementedError("This backend doesn't support local file paths.")
