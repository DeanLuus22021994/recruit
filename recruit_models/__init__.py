"""Models package for the recruit application."""

# Import all models to make them available at package level
# Import STATUS_CHOICES from recruit_types since it's not defined in interviews.py
from recruit_types.interviews import STATUS_CHOICES

from .accounts import UserProfile, create_account_emailaddress
from .candidates import Candidate, CandidateDocument, CandidateRequirements
from .candidates import update_user_profile as candidate_update_user_profile
from .employers import Employer, EmployerImages, EmployerRequirements
from .employers import update_user_profile as employer_update_user_profile
from .interviews import (
    Available,
    Exclusion,
    InterviewInvitation,
    InterviewRequest,
    generate_invitation,
)
from .jobs import Country, Job, JobRequirements
from .recruiters import Recruiter
from .recruiters import update_user_profile as recruiter_update_user_profile
from .sendgrid import EmailLog, EmailTemplate

__all__ = [
    # Accounts models
    "UserProfile",
    "create_account_emailaddress",
    # Candidates models
    "Candidate",
    "CandidateRequirements",
    "CandidateDocument",
    "candidate_update_user_profile",
    # Employers models
    "Employer",
    "EmployerRequirements",
    "EmployerImages",
    "employer_update_user_profile",
    # Interviews models
    "InterviewInvitation",
    "InterviewRequest",
    "Available",
    "Exclusion",
    "generate_invitation",
    "STATUS_CHOICES",
    # Jobs models
    "Country",
    "Job",
    "JobRequirements",
    # Recruiters models
    "Recruiter",
    "recruiter_update_user_profile",
    # SendGrid models
    "EmailTemplate",
    "EmailLog",
]
