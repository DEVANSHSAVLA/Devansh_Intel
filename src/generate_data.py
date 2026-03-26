import pandas as pd
import numpy as np
import random
import os

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Constants for synthetic data
CITIES = ["Mumbai", "Bangalore", "Pune", "Delhi", "Hyderabad", "Remote"]
ROLES = ["Data Scientist", "Web Developer", "ML Engineer", "Backend Developer", "Frontend Developer", "DevOps Engineer"]
COMPANIES = ["Google", "Microsoft", "TCS", "Infosys", "Amazon", "StartupX", "TechGiant", "InnovateAI"]
SKILL_POOLS = {
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas", "Scikit-Learn", "NLTK"],
    "Web Developer": ["JavaScript", "HTML", "CSS", "React", "Node.js", "Django", "Flask"],
    "ML Engineer": ["Python", "TensorFlow", "PyTorch", "Spark", "Docker", "AWS", "Machine Learning"],
    "Backend Developer": ["Java", "Python", "SQL", "Go", "Kubernetes", "Redis", "API Design"],
    "Frontend Developer": ["JavaScript", "TypeScript", "React", "Vue", "Redux", "Sass"],
    "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD", "Linux", "Jenkins"]
}
EDUCATION_LEVELS = ["B.Tech", "M.Tech", "MBA", "PhD", "Any Graduate"]
SALARY_RANGES = {
    "Entry Level": (500000, 800000),
    "Mid Level": (1000000, 1800000),
    "Senior Level": (2000000, 4500000)
}

def generate_description(role, skills, exp_years, edu):
    intro = f"Join {random.choice(COMPANIES)} as a {role}. We are looking for talented individuals with {exp_years}+ years of experience."
    req = f"Requirements: {edu} degree required. Must have strong experience in {', '.join(skills[:3])}. Knowledge of {', '.join(skills[3:])} is a plus."
    return f"{intro} {req}"

def create_synthetic_jobs(n=200):
    data = []
    for _ in range(n):
        role = random.choice(ROLES)
        city = random.choice(CITIES)
        company = random.choice(COMPANIES)
        exp_level = random.choice(EXPERIENCE_LEVELS)
        
        # New v2.0 Fields
        exp_years = random.randint(0, 2) if exp_level == "Entry Level" else random.randint(3, 7) if exp_level == "Mid Level" else random.randint(8, 15)
        edu = random.choice(EDUCATION_LEVELS)
        sal_min, sal_max = SALARY_RANGES[exp_level]
        sal_min += random.randint(-50000, 50000)
        sal_max += random.randint(-100000, 100000)
        
        # Add random date in last 12 months
        days_ago = random.randint(0, 365)
        date = pd.Timestamp.now() - pd.Timedelta(days=days_ago)
        
        # Pick 4-6 skills from the pool for that role
        role_skills = SKILL_POOLS[role]
        num_skills = random.randint(4, 7)
        skills = random.sample(role_skills, min(num_skills, len(role_skills)))
        
        # Add some random generic skills
        if random.random() > 0.5:
            skills.append(random.choice(["Communication", "Teamwork", "Agile"]))
            
        desc = generate_description(role, skills, exp_years, edu)
        
        data.append({
            "Job Title": role,
            "Company": company,
            "Location": city,
            "Experience Level": exp_level,
            "Experience Required (Yrs)": exp_years,
            "Education": edu,
            "Salary Min": sal_min,
            "Salary Max": sal_max,
            "Date": date.strftime('%Y-%m-%d'),
            "Job Description": desc
        })
    
    df = pd.DataFrame(data)
    df.to_csv('data/jobs_raw.csv', index=False)
    print(f"Generated {n} synthetic jobs and saved to data/jobs_raw.csv")

if __name__ == "__main__":
    create_synthetic_jobs(500)
