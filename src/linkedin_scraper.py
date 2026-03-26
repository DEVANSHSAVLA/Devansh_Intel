import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

def scrape_linkedin_mock(keywords=["AI", "Data Science"], locations=["Bangalore", "Mumbai"]):
    """
    Simulated scraper logic for LinkedIn trend analysis.
    In a production MAANG-tier system, this would use Proxies + Headless Browsers.
    """
    data = []
    for kw in keywords:
        for loc in locations:
            # Simulate scraping 5-10 jobs per keyword/location pair
            for i in range(random.randint(5, 10)):
                data.append({
                    "Job Title": f"{kw} Specialist {i}",
                    "Location": loc,
                    "Skills": random.sample(["Python", "AWS", "SQL", "React", "TensorFlow", "Spark", "Docker"], 3),
                    "Demand Score": random.randint(70, 99)
                })
    return pd.DataFrame(data)

def get_skill_role_matrix(df):
    """Generates a matrix of Skill vs Role demand."""
    all_skills = list(set([s for sk in df['Skills'] for s in sk]))
    roles = df['Job Title'].unique()
    matrix = pd.DataFrame(0, index=roles, columns=all_skills)
    
    for _, row in df.iterrows():
        for s in row['Skills']:
            matrix.at[row['Job Title'], s] += 1
            
    return matrix

def get_city_skill_heatmap(df):
    """Generates demand intensity of top 10 skills by city."""
    city_skills = df.explode('Skills')
    heatmap_data = city_skills.groupby(['Location', 'Skills']).size().unstack(fill_value=0)
    return heatmap_data.head(10) # Top cities/skills
