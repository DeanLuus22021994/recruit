from typing import Any

from django.conf import settings

try:
    from storages.backends.s3boto3 import S3Boto3Storage  # type: ignore[import-untyped]
except ImportError:
    # Fallback for older versions
    try:
        from storages.backends.s3boto import (
            S3BotoStorage as S3Boto3Storage,  # type: ignore[import-untyped]
        )
    except ImportError:
        # Final fallback
        from django.core.files.storage import DefaultStorage as S3Boto3Storage


class StaticStorage(S3Boto3Storage):  # type: ignore[misc]
    location = settings.STATICFILES_LOCATION

    def get_accessed_time(self, name: str) -> Any:
        raise NotImplementedError("This backend doesn't support accessed time.")

    def get_created_time(self, name: str) -> Any:
        raise NotImplementedError("This backend doesn't support created time.")

    def path(self, name: str) -> str:
        raise NotImplementedError("This backend doesn't support local file paths.")


class MediaStorage(S3Boto3Storage):  # type: ignore[misc]
    location = settings.MEDIAFILES_LOCATION

    def get_accessed_time(self, name: str) -> Any:
        raise NotImplementedError("This backend doesn't support accessed time.")

    def get_created_time(self, name: str) -> Any:
        raise NotImplementedError("This backend doesn't support created time.")

    def path(self, name: str) -> str:
        raise NotImplementedError("This backend doesn't support local file paths.")
