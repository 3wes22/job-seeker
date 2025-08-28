from django.test import TestCase
from .models import Company, Job
# from .models import Company, Job, JobCategory, JobSkill
from django.contrib.auth.models import User


class JobModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            industry="Technology",
            size="Medium",
            location="New York"
        )
        # self.category = JobCategory.objects.create(
        #     name="Software Development"
        # )
        # self.skill = JobSkill.objects.create(
        #     name="Python"
        # )
        self.job = Job.objects.create(
            title="Software Engineer",
            description="A software engineering position",
            requirements="Python, Django, React",
            company=self.company,
            employer_id=1,
            job_type="Full-time",
            experience_level="Mid-level",
            location="New York",
            is_remote=False,
            salary_min=80000,
            salary_max=120000
        )

    def test_job_creation(self):
        self.assertEqual(self.job.title, "Software Engineer")
        self.assertEqual(self.job.company, self.company)
        self.assertEqual(self.job.job_type, "full_time")

    def test_job_salary_range(self):
        self.job.salary_min = 80000
        self.job.salary_max = 120000
        self.job.salary_currency = "USD"
        self.assertEqual(self.job.salary_range, "USD 80,000 - 120,000")


class CompanyModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            description="A test company",
            industry="Technology",
            employer_id=1
        )

    def test_company_creation(self):
        self.assertEqual(self.company.name, "Test Company")
        self.assertEqual(self.company.industry, "Technology")
        self.assertFalse(self.company.is_verified) 