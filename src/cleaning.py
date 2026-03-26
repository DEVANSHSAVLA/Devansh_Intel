import pandas as pd
import re
import os

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove special characters except common punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,?!#+]', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    # Lowercase
    return text.lower()

def clean_data(input_path='data/jobs_raw.csv', output_path='data/jobs_cleaned.csv'):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    df = pd.read_csv(input_path)
    print(f"Initial shape: {df.shape}")

    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Handle missing values
    df.fillna("Not Specified", inplace=True)
    
    # Clean job descriptions
    df['Cleaned Description'] = df['Job Description'].apply(clean_text)
    
    # Normalize job titles
    df['Job Title'] = df['Job Title'].apply(lambda x: x.strip())
    
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}. Final shape: {df.shape}")

if __name__ == "__main__":
    clean_data()
