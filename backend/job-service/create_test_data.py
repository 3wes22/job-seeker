#!/usr/bin/env python3
"""
Simple script to create test data for the job service
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_service.settings')
django.setup()

from jobs.models import Company, Job
from django.utils import timezone

def create_test_data():
    print("Creating test data...")
    
    # Create a test company
    company, created = Company.objects.get_or_create(
        name="Test Tech Company",
        defaults={
            'industry': 'Technology',
            'size': 'medium',
            'location': 'San Francisco, CA',
            'is_verified': True
        }
    )
    
    if created:
        print(f"✓ Created company: {company.name}")
    else:
        print(f"✓ Company already exists: {company.name}")
    
    # Create a test job
    job, created = Job.objects.get_or_create(
        title="Software Engineer",
        defaults={
            'description': 'We are looking for a talented software engineer...',
            'requirements': 'Python, Django, React experience required',
            'responsibilities': 'Develop and maintain web applications',
            'company': company,
            'employer_id': 1,
            'job_type': 'full_time',
            'experience_level': 'mid',
            'location': 'San Francisco, CA',
            'is_remote': False,
            'is_active': True,
            'salary_min': 80000,
            'salary_max': 120000,
            'salary_currency': 'USD'
        }
    )
    
    if created:
        print(f"✓ Created job: {job.title}")
    else:
        print(f"✓ Job already exists: {job.title}")
    
    print("Test data creation complete!")
    print(f"Company: {company.name}")
    print(f"Job: {job.title} at {job.company.name}")

if __name__ == '__main__':
    create_test_data()
