import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

def train_role_demand(df):
    # Convert dates to month-year and count jobs per role
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M').astype(str)
    
    role_trends = df.groupby(['Month', 'Job Title']).size().reset_index(name='JobCount')
    
    # Month encoding
    months = sorted(role_trends['Month'].unique())
    month_map = {m: i for i, m in enumerate(months)}
    role_trends['Month_Idx'] = role_trends['Month'].map(month_map)
    
    models = {}
    for role in role_trends['Job Title'].unique():
        role_data = role_trends[role_trends['Job Title'] == role]
        if len(role_data) > 1:
            X = role_data[['Month_Idx']]
            y = role_data['JobCount']
            model = LinearRegression()
            model.fit(X, y)
            models[role] = model
            
    if not os.path.exists('models'):
        os.makedirs('models')
    joblib.dump({
        'models': models,
        'month_map': month_map,
        'last_month_idx': max(month_map.values())
    }, 'models/role_trends.pkl')
    print("Role demand forecasting models trained.")

if __name__ == "__main__":
    if os.path.exists('data/jobs_cleaned_with_skills.csv'):
        df = pd.read_csv('data/jobs_cleaned_with_skills.csv')
        train_role_demand(df)
