"""Models package for the recruit application."""

# Import all models to make them available at package level
from .accounts import UserProfile
from .candidates import Candidate, CandidateRequirements, CandidateDocument
from .employers import Employer, EmployerRequirements, EmployerImages
from .interviews import InterviewInvitation, InterviewRequest, Available, Exclusion
from .jobs import Country, Job, JobRequirements
from .recruiters import Recruiter
from .sendgrid import EmailTemplate, EmailLog

__all__ = [
    # Accounts models
    'UserProfile',
    # Candidates models
    'Candidate',
    'CandidateRequirements',
    'CandidateDocument',
    # Employers models
    'Employer',
    'EmployerRequirements',
    'EmployerImages',
    # Interviews models
    'InterviewInvitation',
    'InterviewRequest',
    'Available',
    'Exclusion',
    # Jobs models
    'Country',
    'Job',
    'JobRequirements',
    # Recruiters models
    'Recruiter',
    # SendGrid models
    'EmailTemplate',
    'EmailLog',
]