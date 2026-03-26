import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
import joblib
import ast
import os

def prepare_salary_data(df):
    # Features: Role, City, Experience, Skills (Binarized)
    le_role = LabelEncoder()
    le_city = LabelEncoder()
    
    df['Role_Enc'] = le_role.fit_transform(df['Job Title'])
    df['City_Enc'] = le_city.fit_transform(df['Location'])
    
    # Binarize skills
    df['Extracted Skills'] = df['Extracted Skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    mlb = MultiLabelBinarizer()
    skills_encoded = mlb.fit_transform(df['Extracted Skills'])
    skills_columns = [f"skill_{s}" for s in mlb.classes_]
    skills_df = pd.DataFrame(skills_encoded, columns=skills_columns)
    
    X = pd.concat([
        df[['Role_Enc', 'City_Enc', 'Experience Required (Yrs)']],
        skills_df
    ], axis=1)
    
    y = (df['Salary Min'] + df['Salary Max']) / 2
    
    # Save encoders
    if not os.path.exists('models'):
        os.makedirs('models')
    joblib.dump({
        'le_role': le_role,
        'le_city': le_city,
        'mlb': mlb,
        'skills_columns': skills_columns
    }, 'models/salary_encoders.pkl')
    
    return X, y

def train_salary_model(X, y):
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X, y)
    joblib.dump(model, 'models/salary_model.pkl')
    print("Salary prediction model trained and saved to models/salary_model.pkl")

if __name__ == "__main__":
    if os.path.exists('data/jobs_cleaned_with_skills.csv'):
        df = pd.read_csv('data/jobs_cleaned_with_skills.csv')
        X, y = prepare_salary_data(df)
        train_salary_model(X, y)
    else:
        print("Required data file not found.")
