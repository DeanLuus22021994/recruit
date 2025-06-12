"""Models for the candidates application."""

# Import models from centralized location
from recruit_models.candidates import (
    Candidate,
    CandidateDocument,
    CandidateRequirements,
    update_user_profile,
)

__all__ = [
    "Candidate",
    "CandidateRequirements",
    "CandidateDocument",
    "update_user_profile",
]
