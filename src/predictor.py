import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import ast
import os

def prepare_ml_data(df):
    # Explode skills to have one skill per row
    df['Extracted Skills'] = df['Extracted Skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    df_exploded = df.explode('Extracted Skills')
    
    # Calculate demand: Count frequency of each skill per Role + City + Month
    df_exploded['Month'] = pd.to_datetime(df_exploded['Date']).dt.to_period('M').astype(str)
    
    demand = df_exploded.groupby(['Job Title', 'Location', 'Month', 'Extracted Skills']).size().reset_index(name='Demand')
    
    # Feature Encoding
    le_role = LabelEncoder()
    le_city = LabelEncoder()
    le_skill = LabelEncoder()
    
    demand['Role_Enc'] = le_role.fit_transform(demand['Job Title'])
    demand['City_Enc'] = le_city.fit_transform(demand['Location'])
    demand['Skill_Enc'] = le_skill.fit_transform(demand['Extracted Skills'])
    
    # Month encoding (relative to start)
    months = sorted(demand['Month'].unique())
    month_map = {m: i for i, m in enumerate(months)}
    demand['Month_Enc'] = demand['Month'].map(month_map)
    
    # Save encoders for later use in app
    if not os.path.exists('models'):
        os.makedirs('models')
    joblib.dump({
        'le_role': le_role, 
        'le_city': le_city, 
        'le_skill': le_skill,
        'month_map': month_map,
        'months': months
    }, 'models/encoders.pkl')
    
    return demand

def train_model(demand_df):
    X = demand_df[['Role_Enc', 'City_Enc', 'Skill_Enc', 'Month_Enc']]
    y = demand_df['Demand']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, 'models/model.pkl')
    print("Model trained and saved to models/model.pkl")

if __name__ == "__main__":
    if os.path.exists('data/jobs_cleaned_with_skills.csv'):
        df = pd.read_csv('data/jobs_cleaned_with_skills.csv')
        demand_df = prepare_ml_data(df)
        train_model(demand_df)
    else:
        print("Required data file not found.")
