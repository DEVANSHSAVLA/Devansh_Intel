import pandas as pd
import os
import numpy as np

# Skill difficulty and learning time (estimated)
SKILL_METRICS = {
    "python": {"difficulty": "Easy", "months": 2},
    "sql": {"difficulty": "Easy", "months": 1.5},
    "machine learning": {"difficulty": "Hard", "months": 5},
    "deep learning": {"difficulty": "Hard", "months": 6},
    "aws": {"difficulty": "Medium", "months": 3},
    "docker": {"difficulty": "Medium", "months": 2},
    "kubernetes": {"difficulty": "Hard", "months": 4},
    "react": {"difficulty": "Medium", "months": 3},
    "javascript": {"difficulty": "Medium", "months": 2},
    "java": {"difficulty": "Hard", "months": 4},
}

def get_simulator_pro(current_skills, target_role, data_path='data/jobs_cleaned_with_skills.csv'):
    from src.recommender import get_recommendations
    recs = get_recommendations(current_skills, target_role, data_path)
    
    if "error" in recs:
        return recs
    
    missing = recs['recommended']
    current_skills_lower = [s.lower() for s in current_skills]
    
    # Path logic
    path = []
    total_months = 0
    total_difficulty_score = 0
    
    for skill in missing:
        metric = SKILL_METRICS.get(skill.lower(), {"difficulty": "Medium", "months": 2.5})
        path.append({
            "skill": skill,
            "difficulty": metric["difficulty"],
            "months": metric["months"]
        })
        total_months += metric["months"]
        diff_val = 1 if metric["difficulty"] == "Easy" else 2 if metric["difficulty"] == "Medium" else 3
        total_difficulty_score += diff_val
        
    # Risk factor: based on % of skills missing
    risk_score = (len(missing) / len(recs['top_skills'])) * 100 if recs['top_skills'] else 100
    risk_level = "High" if risk_score > 60 else "Moderate" if risk_score > 30 else "Low"
    
    return {
        "target": target_role,
        "path": path,
        "total_estimated_months": round(total_months, 1),
        "risk_level": risk_level,
        "overall_difficulty": "Hard" if (total_difficulty_score / len(missing) if missing else 0) > 2.5 else "Moderate"
    }

if __name__ == "__main__":
    print(get_simulator_pro(["Python", "SQL"], "Machine Learning Engineer"))
