#!/usr/bin/env python3
"""
Test script to verify model imports work correctly.
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruit.settings")
import django

django.setup()

try:
    # Test recruit_models imports
    print("Testing recruit_models imports...")

    from recruit_models.accounts import UserProfile

    print("✓ accounts models imported successfully")

    from recruit_models.candidates import (
        Candidate,
    )

    print("✓ candidates models imported successfully")

    from recruit_models.employers import Employer

    print("✓ employers models imported successfully")

    from recruit_models.interviews import InterviewInvitation

    print("✓ interviews models imported successfully")

    from recruit_models.jobs import Job

    print("✓ jobs models imported successfully")

    from recruit_models.recruiters import Recruiter

    print("✓ recruiters models imported successfully")

    from recruit_models.sendgrid import EmailTemplate

    print("✓ sendgrid models imported successfully")

    # Test app-level imports
    from accounts.models import UserProfile as AppUserProfile

    print("✓ accounts app models imported successfully")

    from candidates.models import Candidate as AppCandidate

    print("✓ candidates app models imported successfully")

    from employers.models import Employer as AppEmployer

    print("✓ employers app models imported successfully")

    from interviews.models import InterviewInvitation as AppInterview

    print("✓ interviews app models imported successfully")

    from jobs.models import Job as AppJob

    print("✓ jobs app models imported successfully")

    from recruiters.models import Recruiter as AppRecruiter

    print("✓ recruiters app models imported successfully")

    from sendgrid.models import EmailTemplate as AppEmailTemplate

    print("✓ sendgrid app models imported successfully")

    # Verify they are the same objects
    print("\nVerifying model identity...")
    assert UserProfile is AppUserProfile, "UserProfile models should be identical"
    assert Candidate is AppCandidate, "Candidate models should be identical"
    assert Employer is AppEmployer, "Employer models should be identical"
    assert InterviewInvitation is AppInterview, "Interview models should be identical"
    assert Job is AppJob, "Job models should be identical"
    assert Recruiter is AppRecruiter, "Recruiter models should be identical"
    assert EmailTemplate is AppEmailTemplate, "EmailTemplate models should be identical"
    print("✓ All model identities verified")

    print("\n🎉 All imports successful! Model refactoring is working correctly.")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except AssertionError as e:
    print(f"❌ Assertion error: {e}")
    sys.exit(1)
