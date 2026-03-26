import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os

def analyze_keywords(df, text_col='Cleaned Description'):
    if df.empty: return []
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=20)
    tfidf_matrix = vectorizer.fit_transform(df[text_col])
    
    feature_names = vectorizer.get_feature_names_out()
    sums = tfidf_matrix.sum(axis=0)
    
    data = []
    for col, i in enumerate(sums.tolist()[0]):
        data.append((feature_names[col], i))
        
    ranking = sorted(data, key=lambda x: x[1], reverse=True)
    return ranking

def get_sentiment_simple(text):
    # Simple rule-based sentiment for urgency
    urgency_keywords = ['urgent', 'immediate', 'hiring now', 'fast-track', 'asap']
    text_lower = text.lower()
    score = sum(1 for word in urgency_keywords if word in text_lower)
    return "High" if score > 0 else "Normal"

if __name__ == "__main__":
    if os.path.exists('data/jobs_cleaned.csv'):
        df = pd.read_csv('data/jobs_cleaned.csv')
        top_keywords = analyze_keywords(df)
        print("Top Keywords (TF-IDF):", top_keywords)
