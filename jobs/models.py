from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    pass
else:
    pass


class Country(models.Model):
    country: models.CharField = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.country)


class Job(models.Model):
    employer: models.ForeignKey = models.ForeignKey(
        "employers.Employer", on_delete=models.CASCADE, related_name="jobs"
    )
    title: models.CharField = models.CharField(max_length=100)
    location: models.CharField = models.CharField(
        choices=(("onsite", "On-site"), ("remote", "Remote")),
        max_length=50,
        blank=True,
        null=True,
    )
    weekly_hours: models.IntegerField = models.IntegerField()
    salary_high: models.IntegerField = models.IntegerField()
    salary_low: models.IntegerField = models.IntegerField()
    accommodation_included: models.BooleanField = models.BooleanField()
    accommodation_stipend: models.CharField = models.CharField(max_length=100)
    travel_stipend: models.CharField = models.CharField(max_length=100)
    insurance_included: models.BooleanField = models.BooleanField()
    insurance_stipend: models.CharField = models.CharField(max_length=100)
    contract_length: models.IntegerField = models.IntegerField()
    contract_renew_bonus: models.IntegerField = models.IntegerField(
        blank=True, null=True
    )
    contract_completion_bonus: models.IntegerField = models.IntegerField(
        blank=True, null=True
    )
    compensation_type: models.CharField = models.CharField(
        max_length=25,
        blank=False,
        choices=(
            ("One-time", "One-time"),
            ("Monthly", "Monthly"),
        ),
    )
    compensation_amount: models.CharField = models.CharField(max_length=25, blank=False)
    compensation_terms: models.CharField = models.CharField(max_length=250)
    is_featured: models.BooleanField = models.BooleanField(default=False)
    is_active: models.BooleanField = models.BooleanField(default=True)
    recruiter: models.ForeignKey = models.ForeignKey(
        "recruiters.Recruiter", on_delete=models.CASCADE, related_name="jobs"
    )
    last_modified: models.DateTimeField = models.DateTimeField(
        auto_now_add=False, auto_now=True
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, auto_now=False
    )

    def __str__(self) -> str:
        employer_name = getattr(self.employer, "name_english", "Unknown")
        return f"{self.pk}) {employer_name}: {self.title}"


class JobRequirements(models.Model):
    job: models.OneToOneField = models.OneToOneField(Job, on_delete=models.CASCADE)
    age_high: models.IntegerField = models.IntegerField()
    age_low: models.IntegerField = models.IntegerField()
    gender: models.CharField = models.CharField(
        choices=(("male", "Male"), ("female", "Female")),
        max_length=10,
        blank=True,
        null=True,
    )
    citizenship: models.ManyToManyField = models.ManyToManyField(Country, blank=True)

    def __str__(self) -> str:
        job_title = getattr(self.job, "title", "Unknown Job")
        return f"Requirements for {job_title}"
