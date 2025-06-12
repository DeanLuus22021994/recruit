"""Utility functions for file processing and S3 operations."""

import mimetypes
from io import BytesIO
from typing import Any, List

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def generate_thumbnail(file: Any) -> SimpleUploadedFile:
    """Generate a thumbnail from an uploaded image file."""
    size = (100, 100)
    im = Image.open(file)
    filename = file.name.split("/")[-1].split(".")[0]
    mime = mimetypes.guess_type(file.name)[0]

    if not mime:
        mime = "image/jpeg"  # Default fallback

    file_type = mime.split("/")[-1]
    filename = filename + "-thumb." + file_type
    im.thumbnail(size)
    memory_file = BytesIO()
    im.save(memory_file, file_type.upper())
    suf = SimpleUploadedFile(filename, memory_file.getvalue(), content_type=mime)
    return suf


def delete_from_s3(instances_list: List[Any]) -> List[Any]:
    """Delete files from S3 storage for given instances."""
    for instance in instances_list:
        if hasattr(instance, "storage") and hasattr(instance, "name"):
            instance.storage.delete(name=instance.name)
    return instances_list
