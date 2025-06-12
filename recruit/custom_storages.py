# filepath: c:\Projects\recruit\recruit\custom_storages.py
from django.conf import settings

try:
    from storages.backends.s3boto3 import S3Boto3Storage
except ImportError:
    # Fallback for older versions
    try:
        from storages.backends.s3boto import (
            S3BotoStorage as S3Boto3Storage,  # type: ignore[misc]
        )
    except ImportError:
        # Final fallback
        from django.core.files.storage import (
            DefaultStorage as S3Boto3Storage,  # type: ignore[misc]
        )


class StaticStorage(S3Boto3Storage):  # type: ignore[misc]
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):  # type: ignore[misc]
    location = settings.MEDIAFILES_LOCATION
