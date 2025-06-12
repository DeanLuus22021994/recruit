"""Django app configuration for jobs application."""

from django.apps import AppConfig


class JobsConfig(AppConfig):
    """Configuration for the jobs app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "jobs"
