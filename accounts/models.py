"""Models for the accounts application."""

# Import models from centralized location
from recruit_models.accounts import UserProfile, create_account_emailaddress

__all__ = ["UserProfile", "create_account_emailaddress"]
