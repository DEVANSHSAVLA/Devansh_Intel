import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
import re
import os

# Skill list - can be expanded
SKILLS = [
    "python", "java", "javascript", "sql", "machine learning", "react", "aws", 
    "docker", "kubernetes", "tensorflow", "pytorch", "node.js", "django", "flask", 
    "statistics", "tableau", "power bi", "excel", "spark", "hadoop", "c++", "c#", 
    "php", "ruby", "swift", "kotlin", "go", "rust", "html", "css", "typescript", 
    "vue", "angular", "git", "ci/cd", "agile", "scrum", "cloud computing", "azure", 
    "gcp", "mongodb", "postgresql", "mysql", "redis", "elasticsearch"
]

def extract_years_exp(text):
    match = re.search(r'(\d+)\s*[\+\-]*\s*years?', text, re.IGNORECASE)
    return int(match.group(1)) if match else 0

def extract_education(text):
    levels = ["B.Tech", "M.Tech", "MBA", "PhD", "B.Sc", "M.Sc", "Bachelor", "Master"]
    for level in levels:
        if re.search(r'\b' + re.escape(level) + r'\b', text, re.IGNORECASE):
            return level
    return "Not Specified"

def extract_skills(text, nlp, matcher):
    if not text:
        return []
    doc = nlp(text)
    matches = matcher(doc)
    extracted = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        extracted.add(span.text.lower())
    return list(extracted)

def process_skills(input_path='data/jobs_cleaned.csv', output_path='data/jobs_cleaned_with_skills.csv'):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    # Load spaCy model
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("SpaCy model 'en_core_web_sm' not found. Please install it.")
        return

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in SKILLS]
    matcher.add("SkillMatcher", patterns)

    df = pd.read_csv(input_path)
    
    print("Extracting skills, experience, and education...")
    target_col = 'Cleaned Description' if 'Cleaned Description' in df.columns else 'Job Description'
    
    df['Extracted Skills'] = df[target_col].apply(lambda x: extract_skills(x, nlp, matcher))
    df['Extracted Exp'] = df[target_col].apply(extract_years_exp)
    df['Extracted Education'] = df[target_col].apply(extract_education)
    
    # Save the result
    df.to_csv(output_path, index=False)
    print(f"Extraction complete. Saved to {output_path}")

if __name__ == "__main__":
    process_skills()
