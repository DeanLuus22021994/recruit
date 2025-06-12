"""Models for the jobs application."""

from django.db import models


class Country(models.Model):
    """Model representing a country."""

    country = models.CharField(max_length=100)

    class Meta:
        app_label = "jobs"

    def __str__(self) -> str:
        """Return string representation of the country."""
        return str(self.country)


class Job(models.Model):
    """Model representing a job posting."""    employer = models.ForeignKey(
        "recruit_models.Employer", on_delete=models.CASCADE, related_name="jobs"
    )
    title = models.CharField(max_length=100)
    location = models.CharField(
        choices=(("onsite", "On-site"), ("remote", "Remote")),
        max_length=50,
        blank=True,
        null=True,
    )
    weekly_hours = models.IntegerField()
    salary_high = models.IntegerField()
    salary_low = models.IntegerField()
    accommodation_included = models.BooleanField()
    accommodation_stipend = models.CharField(max_length=100)
    travel_stipend = models.CharField(max_length=100)
    insurance_included = models.BooleanField()
    insurance_stipend = models.CharField(max_length=100)
    contract_length = models.IntegerField()
    contract_renew_bonus = models.IntegerField(blank=True, null=True)
    contract_completion_bonus = models.IntegerField(blank=True, null=True)
    compensation_type = models.CharField(
        max_length=25,
        blank=False,
        choices=(
            ("One-time", "One-time"),
            ("Monthly", "Monthly"),
        ),
    )
    compensation_amount = models.CharField(max_length=25, blank=False)
    compensation_terms = models.CharField(max_length=250)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    recruiter = models.ForeignKey(
        "models.Recruiter", on_delete=models.CASCADE, related_name="jobs"
    )
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        app_label = "jobs"

    def __str__(self) -> str:
        """Return string representation of the job."""
        employer_name = getattr(self.employer, "name_english", "Unknown")
        return f"{self.pk}) {employer_name}: {self.title}"


class JobRequirements(models.Model):
    """Model representing job requirements."""

    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    age_high = models.IntegerField()
    age_low = models.IntegerField()
    gender = models.CharField(
        choices=(("male", "Male"), ("female", "Female")),
        max_length=10,
        blank=True,
        null=True,
    )
    citizenship = models.ManyToManyField(Country, blank=True)

    class Meta:
        app_label = "jobs"

    def __str__(self) -> str:
        """Return string representation of the job requirements."""
        job_title = getattr(self.job, "title", "Unknown Job")
        return f"Requirements for {job_title}"
