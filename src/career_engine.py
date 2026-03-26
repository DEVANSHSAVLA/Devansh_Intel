import pandas as pd
import ast
import os
from collections import Counter

def get_related_skills(skill, data_path='data/jobs_cleaned_with_skills.csv'):
    if not os.path.exists(data_path):
        return []
    
    df = pd.read_csv(data_path)
    df['Extracted Skills'] = df['Extracted Skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    # Find jobs where this skill is mentioned
    related = []
    for skills in df['Extracted Skills']:
        if skill.lower() in [s.lower() for s in skills]:
            related.extend([s for s in skills if s.lower() != skill.lower()])
            
    counts = Counter(related)
    return [s for s, _ in counts.most_common(5)]

def career_simulator(current_skills, target_role, data_path='data/jobs_cleaned_with_skills.csv'):
    # Logic: Current Skills -> Missing Skills -> Path
    from src.recommender import get_recommendations
    recs = get_recommendations(current_skills, target_role, data_path)
    
    if "error" in recs:
        return recs
        
    path = []
    missing = recs['recommended']
    
    if len(missing) == 0:
        return {"status": "Ready", "message": f"You are ready for {target_role}!"}
        
    # Simulate months based on number of missing skills
    months = len(missing) * 1.5 # Assign 1.5 months per major skill
    
    path.append(f"Month 0-3: Focus on {', '.join(missing[:2])}")
    if len(missing) > 2:
        path.append(f"Month 4-{int(months)}: Master {', '.join(missing[2:])}")
    path.append(f"Target: Become a {target_role}")
    
    return {
        "target": target_role,
        "estimated_months": int(months),
        "steps": path
    }

if __name__ == "__main__":
    print(get_related_skills("Python"))
    print(career_simulator(["Python", "SQL"], "Data Scientist"))
