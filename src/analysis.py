import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os

def load_data(path='data/jobs_cleaned_with_skills.csv'):
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    # Convert string representation of list to actual list
    def safe_literal_eval(x):
        try:
            return ast.literal_eval(x) if isinstance(x, str) else x
        except:
            return []
    df['Extracted Skills'] = df['Extracted Skills'].apply(safe_literal_eval)
    return df

def analyze_trends(df):
    if df is None: return
    
    # Ensure notebooks directory exists
    if not os.path.exists('notebooks'):
        os.makedirs('notebooks')

    # 1. Top Skills Overall
    all_skills = [skill for skills in df['Extracted Skills'] for skill in skills]
    if not all_skills:
        print("No skills found to analyze.")
        return
        
    skill_counts = pd.Series(all_skills).value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=skill_counts.values, y=skill_counts.index, palette='viridis')
    plt.title('Top 10 Most Demanded Skills')
    plt.xlabel('Frequency')
    plt.tight_layout()
    plt.savefig('notebooks/top_skills_overall.png')
    plt.close()

    # 2. Skills by Role
    print("Generating role-based skill distribution...")
    # Explode the skills list
    df_exploded = df.explode('Extracted Skills')
    
    # Get top 5 skills for top roles
    top_roles = df['Job Title'].value_counts().head(5).index
    for role in top_roles:
        role_skills = df_exploded[df_exploded['Job Title'] == role]['Extracted Skills'].value_counts().head(5)
        if not role_skills.empty:
            plt.figure(figsize=(8, 5))
            sns.barplot(x=role_skills.values, y=role_skills.index)
            plt.title(f'Top 5 Skills for {role}')
            plt.tight_layout()
            plt.savefig(f'notebooks/top_skills_{role.replace(" ", "_")}.png')
            plt.close()

    # 3. Job Distribution by City
    plt.figure(figsize=(8, 8))
    city_counts = df['Location'].value_counts()
    plt.pie(city_counts, labels=city_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Job Distribution by City')
    plt.savefig('notebooks/job_distribution_city.png')
    plt.close()

if __name__ == "__main__":
    df = load_data()
    if df is not None:
        analyze_trends(df)
        print("Analysis complete. Visualizations saved in notebooks/ directory.")
    else:
        print("Data file not found. Please run skill_extractor.py first.")
