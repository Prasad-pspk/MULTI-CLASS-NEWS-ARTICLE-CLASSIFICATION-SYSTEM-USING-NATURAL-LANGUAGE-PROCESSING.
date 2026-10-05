"""
News Classification Analytics Utilities
Generates detailed analysis and statistics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def generate_analytics_reports():
    """Generate comprehensive analytics reports"""
    
    # Load data
    df = pd.read_csv('/home/ubuntu/news_articles.csv')
    
    # Category statistics
    category_stats = df['category'].value_counts().to_frame()
    category_stats.columns = ['Count']
    category_stats['Percentage'] = (category_stats['Count'] / len(df) * 100).round(2)
    category_stats.to_csv('/home/ubuntu/category_statistics.csv')
    print("✓ Category statistics saved")
    
    # Article length analysis
    df['article_length'] = df['article'].str.len()
    df['word_count'] = df['article'].str.split().str.len()
    
    length_stats = df.groupby('category').agg({
        'article_length': ['min', 'max', 'mean', 'std'],
        'word_count': ['min', 'max', 'mean', 'std']
    }).round(2)
    length_stats.to_csv('/home/ubuntu/article_length_statistics.csv')
    print("✓ Article length statistics saved")
    
    # Keyword frequency analysis
    from collections import Counter
    
    all_words = ' '.join(df['article']).lower().split()
    word_freq = Counter(all_words)
    top_words = pd.DataFrame(word_freq.most_common(50), columns=['Word', 'Frequency'])
    top_words.to_csv('/home/ubuntu/top_keywords.csv', index=False)
    print("✓ Top keywords saved")
    
    # Category-wise word analysis
    for category in df['category'].unique():
        category_text = ' '.join(df[df['category'] == category]['article']).lower()
        words = category_text.split()
        word_freq_cat = Counter(words)
        top_words_cat = pd.DataFrame(word_freq_cat.most_common(20), columns=['Word', 'Frequency'])
        top_words_cat.to_csv(f'/home/ubuntu/keywords_{category.lower()}.csv', index=False)
    print("✓ Category-wise keywords saved")
    
    # Classification performance by category
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['article'])
    
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['category'])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train best model
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    
    # Generate classification report
    report = classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report_df.to_csv('/home/ubuntu/classification_report.csv')
    print("✓ Classification report saved")
    
    # Model comparison
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    
    gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb.fit(X_train, y_train)
    
    models_data = {
        'Model': ['Logistic Regression', 'Random Forest', 'Gradient Boosting'],
        'Accuracy': [
            (lr.predict(X_test) == y_test).mean(),
            (rf.predict(X_test) == y_test).mean(),
            (gb.predict(X_test) == y_test).mean()
        ]
    }
    
    models_df = pd.DataFrame(models_data)
    models_df.to_csv('/home/ubuntu/model_comparison_summary.csv', index=False)
    print("✓ Model comparison summary saved")
    
    # Prediction confidence analysis
    rf_proba = rf.predict_proba(X_test)
    confidence = np.max(rf_proba, axis=1)
    
    confidence_df = pd.DataFrame({
        'Confidence': confidence,
        'Correct': y_pred == y_test,
        'Actual_Category': label_encoder.inverse_transform(y_test),
        'Predicted_Category': label_encoder.inverse_transform(y_pred)
    })
    
    confidence_df.to_csv('/home/ubuntu/prediction_confidence.csv', index=False)
    print("✓ Prediction confidence analysis saved")
    
    print("\n" + "="*60)
    print("ANALYTICS REPORTS GENERATED SUCCESSFULLY")
    print("="*60)

if __name__ == "__main__":
    generate_analytics_reports()
