"""
Dummy data generation for testing the job platform APIs
"""
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

class DummyDataGenerator:
    """Generate realistic dummy data for the job platform"""
    
    def __init__(self):
        self.job_titles = [
            "Senior Software Engineer", "Frontend Developer", "Backend Developer",
            "Full Stack Developer", "DevOps Engineer", "Data Scientist",
            "Product Manager", "UX Designer", "UI Designer", "QA Engineer",
            "Mobile App Developer", "Systems Administrator", "Database Administrator",
            "Security Engineer", "Machine Learning Engineer", "Cloud Architect"
        ]
        
        self.companies = [
            {"name": "TechCorp", "industry": "Technology", "size": "large"},
            {"name": "StartupXYZ", "industry": "Technology", "size": "startup"},
            {"name": "FinanceFlow", "industry": "Finance", "size": "medium"},
            {"name": "HealthTech Solutions", "industry": "Healthcare", "size": "medium"},
            {"name": "EduPlatform", "industry": "Education", "size": "small"},
            {"name": "RetailGiant", "industry": "Retail", "size": "large"},
            {"name": "GreenEnergy Co", "industry": "Energy", "size": "medium"},
            {"name": "MediaMaker", "industry": "Media", "size": "small"},
        ]
        
        self.skills = [
            "Python", "JavaScript", "React", "Node.js", "Django", "Flask",
            "PostgreSQL", "MongoDB", "AWS", "Docker", "Kubernetes", "Git",
            "HTML/CSS", "TypeScript", "Vue.js", "Angular", "Java", "C++",
            "Machine Learning", "Data Analysis", "SQL", "Redis", "GraphQL"
        ]
        
        self.categories = [
            {"name": "Software Development", "description": "Software engineering roles"},
            {"name": "Data Science", "description": "Data analysis and ML roles"},
            {"name": "Design", "description": "UI/UX and graphic design roles"},
            {"name": "DevOps", "description": "Infrastructure and deployment roles"},
            {"name": "Management", "description": "Product and project management roles"},
            {"name": "Quality Assurance", "description": "Testing and QA roles"},
        ]
        
        self.locations = [
            "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
            "Boston, MA", "Chicago, IL", "Los Angeles, CA", "Denver, CO",
            "Remote", "London, UK", "Berlin, Germany", "Toronto, Canada"
        ]
        
        self.first_names = [
            "John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa",
            "James", "Maria", "William", "Jennifer", "Richard", "Susan", "Joseph",
            "Jessica", "Thomas", "Karen", "Christopher", "Nancy", "Daniel", "Betty"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
            "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
            "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
        ]

    def generate_users(self, count: int = 50) -> List[Dict[str, Any]]:
        """Generate dummy users"""
        users = []
        
        for i in range(count):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
            email = f"{username}@example.com"
            
            user = {
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": "testpass123",
                "user_type": random.choice(["job_seeker"] * 7 + ["employer"] * 3),  # 70% job seekers
                "phone_number": f"+1{random.randint(1000000000, 9999999999)}",
                "date_of_birth": (datetime.now() - timedelta(days=random.randint(6570, 18250))).date().isoformat(),
                "bio": f"Experienced professional in {random.choice(['technology', 'finance', 'healthcare', 'education'])}",
                "is_verified": random.choice([True, False]),
                "is_active": True,
            }
            users.append(user)
        
        return users

    def generate_companies(self, count: int = 20) -> List[Dict[str, Any]]:
        """Generate dummy companies"""
        companies = []
        
        base_companies = self.companies * (count // len(self.companies) + 1)
        
        for i in range(count):
            base = base_companies[i]
            company = {
                "name": f"{base['name']} {random.randint(1, 100) if i >= len(self.companies) else ''}".strip(),
                "description": f"Leading company in {base['industry']} industry providing innovative solutions.",
                "website": f"https://www.{base['name'].lower().replace(' ', '')}.com",
                "industry": base['industry'],
                "size": base['size'],
                "founded_year": random.randint(1990, 2020),
                "location": random.choice(self.locations),
                "is_verified": random.choice([True, False]),
            }
            companies.append(company)
        
        return companies

    def generate_jobs(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate dummy jobs"""
        jobs = []
        
        for i in range(count):
            title = random.choice(self.job_titles)
            company_id = random.randint(1, 20)  # Assuming 20 companies
            employer_id = random.randint(1, 15)  # Assuming first 15 users are potential employers
            
            job = {
                "title": title,
                "description": f"We are seeking a talented {title} to join our dynamic team. This role offers exciting opportunities to work on cutting-edge projects and grow your career.",
                "requirements": f"• 3+ years of experience in relevant field\n• Strong problem-solving skills\n• Excellent communication abilities\n• Experience with {', '.join(random.sample(self.skills, 3))}",
                "responsibilities": f"• Develop and maintain high-quality software\n• Collaborate with cross-functional teams\n• Participate in code reviews\n• Mentor junior developers",
                "company_id": company_id,
                "employer_id": employer_id,
                "job_type": random.choice(["full_time", "part_time", "contract", "internship", "freelance"]),
                "experience_level": random.choice(["entry", "mid", "senior", "executive"]),
                "salary_min": random.randint(50000, 120000),
                "salary_max": random.randint(120000, 200000),
                "salary_currency": "USD",
                "location": random.choice(self.locations),
                "is_remote": random.choice([True, False]),
                "is_active": True,
                "application_deadline": (datetime.now() + timedelta(days=random.randint(7, 60))).date().isoformat(),
            }
            jobs.append(job)
        
        return jobs

    def generate_job_categories(self) -> List[Dict[str, Any]]:
        """Generate job categories"""
        return self.categories

    def generate_job_skills(self) -> List[Dict[str, Any]]:
        """Generate job skills"""
        return [{"name": skill} for skill in self.skills]

    def generate_applications(self, count: int = 200) -> List[Dict[str, Any]]:
        """Generate dummy applications"""
        applications = []
        
        for i in range(count):
            application = {
                "job_id": random.randint(1, 100),  # Assuming 100 jobs
                "applicant_id": random.randint(16, 50),  # Job seekers (assuming users 16-50 are job seekers)
                "status": random.choice([
                    "pending", "reviewing", "interview_scheduled", 
                    "interviewed", "offer_extended", "hired", "rejected"
                ]),
                "cover_letter": "I am very interested in this position and believe my skills and experience make me a strong candidate.",
                "additional_data": {
                    "years_of_experience": random.randint(1, 10),
                    "expected_salary": random.randint(60000, 150000),
                },
            }
            applications.append(application)
        
        return applications

    def generate_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate all dummy data"""
        return {
            "users": self.generate_users(50),
            "companies": self.generate_companies(20),
            "job_categories": self.generate_job_categories(),
            "job_skills": self.generate_job_skills(),
            "jobs": self.generate_jobs(100),
            "applications": self.generate_applications(200),
        }

    def save_to_files(self, output_dir: str = "dummy_data"):
        """Save dummy data to JSON files"""
        import os
        
        os.makedirs(output_dir, exist_ok=True)
        data = self.generate_all_data()
        
        for filename, content in data.items():
            filepath = os.path.join(output_dir, f"{filename}.json")
            with open(filepath, 'w') as f:
                json.dump(content, f, indent=2, default=str)
        
        print(f"Dummy data saved to {output_dir}/")

if __name__ == "__main__":
    generator = DummyDataGenerator()
    generator.save_to_files()
    print("Dummy data generation completed!")
