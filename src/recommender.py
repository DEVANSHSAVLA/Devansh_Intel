import pandas as pd
import ast
import os

def get_recommendations(user_skills, target_role, data_path='data/jobs_cleaned_with_skills.csv'):
    if not os.path.exists(data_path):
        return {"error": "Knowledge base not found. Please run the data pipeline first."}

    df = pd.read_csv(data_path)
    df['Extracted Skills'] = df['Extracted Skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    # Filter jobs for the target role
    role_jobs = df[df['Job Title'].str.contains(target_role, case=False)]
    
    if role_jobs.empty:
        return {"error": f"No data found for role: {target_role}"}
    
    # Get all skills required for this role
    required_skills = [skill for skills in role_jobs['Extracted Skills'] for skill in skills]
    skill_series = pd.Series(required_skills).value_counts()
    
    # Normalize skills to lowercase for matching
    user_skills_clean = [s.strip().lower() for s in user_skills]
    
    # Identify top 10 skills for the role
    top_role_skills = skill_series.head(10).index.tolist()
    
    # Find missing skills
    missing_skills = [s for s in top_role_skills if s.lower() not in user_skills_clean]
    
    return {
        "role": target_role,
        "top_skills": top_role_skills,
        "recommended": missing_skills
    }

if __name__ == "__main__":
    # Test
    user_s = ["Python", "SQL"]
    role = "Data Scientist"
    print(get_recommendations(user_s, role))
