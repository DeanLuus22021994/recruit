"""Types package for the recruit application."""

# Import all types to make them available at package level
from ..accounts.types import TokenVerificationResult, UserProfileType
from .candidates import CandidateDocumentType, CandidateRequirementsType, CandidateType
from .employers import EmployerImagesType, EmployerRequirementsType, EmployerType
from .interviews import (
    AvailableType,
    ExclusionType,
    InterviewInvitationType,
    InterviewRequestType,
    StatusChoiceType,
)
from .jobs import CountryType, JobRequirementsType, JobType
from .recruiters import RecruiterType
from .sendgrid import EmailLogType, EmailStatusType, EmailTemplateType

__all__ = [
    # Accounts types
    "UserProfileType",
    "TokenVerificationResult",
    # Candidates types
    "CandidateType",
    "CandidateRequirementsType",
    "CandidateDocumentType",
    # Employers types
    "EmployerType",
    "EmployerRequirementsType",
    "EmployerImagesType",
    # Interviews types
    "InterviewInvitationType",
    "InterviewRequestType",
    "AvailableType",
    "ExclusionType",
    "StatusChoiceType",
    # Jobs types
    "CountryType",
    "JobType",
    "JobRequirementsType",
    # Recruiters types
    "RecruiterType",
    # SendGrid types
    "EmailTemplateType",
    "EmailLogType",
    "EmailStatusType",
]
