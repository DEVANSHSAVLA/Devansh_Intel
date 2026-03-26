import re

BULLET_IMPROVEMENT_MAP = {
    "worked on": "Spearheaded the development of",
    "using": "Leveraged",
    "responsible for": "Orchestrated",
    "improved": "Optimized",
    "accuracy": "model performance and accuracy by 25%",
    "fast": "at scale",
    "built": "Architected and deployed"
}

def analyze_resume_ats(text, target_skills):
    # This node receives high-precision target skills from the Recommender Node
    text_lower = text.lower()
    found = {s: text_lower.count(s.lower()) for s in target_skills if s.lower() in text_lower}
    score = (len(found) / len(target_skills)) * 100 if target_skills else 0
    
    # Improve bullets (Sovereign Engine)
    improved_bullets = []
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        if any(weak in line.lower() for weak in BULLET_IMPROVEMENT_MAP.keys()):
            new_line = line
            for weak, strong in BULLET_IMPROVEMENT_MAP.items():
                new_line = re.sub(re.escape(weak), strong, new_line, flags=re.IGNORECASE)
            improved_bullets.append({"original": line, "improved": new_line})
            if len(improved_bullets) >= 5: break
            
    return {
        "score": round(score, 1),
        "density_map": found,
        "improvements": improved_bullets
    }

if __name__ == "__main__":
    txt = "Worked on ML project using python and improved accuracy."
    print(analyze_resume_ats(txt, ["Python", "Machine Learning", "AWS"]))
