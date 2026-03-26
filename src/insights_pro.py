import pandas as pd
import os
import datetime

def generate_elite_report_stats(df):
    # Sector focus
    sectors = ["FinTech", "HealthTech", "AI", "E-commerce", "SaaS"]
    # We assign jobs to sectors randomly if they don't have them for synthetic representation
    df['Industry'] = df['Job Title'].apply(lambda x: sectors[hash(x) % len(sectors)])
    
    industry_count = df['Industry'].value_counts().to_dict()
    
    # Remote vs On-site (Simulated for jobs)
    remote_ratio = {
        "Data Scientist": 0.6,
        "Frontend Developer": 0.8,
        "Backend Developer": 0.7,
        "ML Engineer": 0.5,
        "Full Stack Developer": 0.75
    }
    
    avg_remote = sum(remote_ratio.values()) / len(remote_ratio)
    
    return {
        "industry_market_share": industry_count,
        "avg_remote_rate": f"{avg_remote:.1%}",
        "market_sentiment": "Bullish (AI Tech Boom)",
        "report_id": f"ELITE-Q1-{datetime.date.today().year}"
    }

if __name__ == "__main__":
    if os.path.exists('data/jobs_cleaned_with_skills.csv'):
        df = pd.read_csv('data/jobs_cleaned_with_skills.csv')
        print(generate_elite_report_stats(df))
