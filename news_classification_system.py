"""
Automated News Article Classification System using NLP and Machine Learning
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

def generate_news_dataset(n_samples=1000):
    """Generate synthetic news articles dataset"""
    np.random.seed(42)
    
    # News categories
    categories = ['Politics', 'Sports', 'Business', 'Entertainment', 'Technology']
    
    # Sample headlines and keywords for each category
    category_data = {
        'Politics': {
            'keywords': ['government', 'election', 'parliament', 'minister', 'policy', 'congress', 'senate', 'vote', 'campaign', 'political'],
            'samples': ['Government announces new policy', 'Election results declared', 'Parliament passes bill', 'Minister addresses nation', 'Political campaign begins']
        },
        'Sports': {
            'keywords': ['match', 'player', 'team', 'score', 'game', 'coach', 'tournament', 'league', 'victory', 'championship'],
            'samples': ['Team wins championship', 'Player scores record goal', 'Tournament begins', 'Coach announces strategy', 'Match highlights']
        },
        'Business': {
            'keywords': ['company', 'market', 'stock', 'revenue', 'profit', 'investment', 'trade', 'finance', 'corporate', 'business'],
            'samples': ['Company reports profit', 'Stock market rises', 'New investment announced', 'Corporate merger', 'Business expansion']
        },
        'Entertainment': {
            'keywords': ['movie', 'actor', 'film', 'celebrity', 'show', 'music', 'concert', 'award', 'entertainment', 'premiere'],
            'samples': ['Movie releases today', 'Celebrity wins award', 'Concert announced', 'Film premiere', 'Music festival begins']
        },
        'Technology': {
            'keywords': ['software', 'technology', 'innovation', 'app', 'digital', 'internet', 'cyber', 'data', 'artificial', 'intelligence'],
            'samples': ['New app launched', 'Technology breakthrough', 'AI innovation', 'Software update', 'Digital transformation']
        }
    }
    
    articles = []
    labels = []
    
    for _ in range(n_samples):
        category = np.random.choice(categories)
        data = category_data[category]
        
        # Generate article text
        num_keywords = np.random.randint(3, 8)
        keywords = np.random.choice(data['keywords'], num_keywords, replace=False)
        sample = np.random.choice(data['samples'])
        
        article_text = sample + ' ' + ' '.join(keywords) + ' ' + ' '.join(np.random.choice(data['keywords'], 2))
        
        articles.append(article_text)
        labels.append(category)
    
    df = pd.DataFrame({'article': articles, 'category': labels})
    return df

def preprocess_text(df):
    """Preprocess text data using TF-IDF"""
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['article'])
    
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['category'])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test, vectorizer, label_encoder

def train_classifiers(X_train, X_test, y_train, y_test):
    """Train classification models"""
    results = {}
    
    # Logistic Regression
    print("Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    results['Logistic Regression'] = {
        'model': lr,
        'predictions': y_pred_lr,
        'accuracy': accuracy_score(y_test, y_pred_lr),
        'precision': precision_score(y_test, y_pred_lr, average='weighted'),
        'recall': recall_score(y_test, y_pred_lr, average='weighted'),
        'f1': f1_score(y_test, y_pred_lr, average='weighted')
    }
    
    # Random Forest
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    results['Random Forest'] = {
        'model': rf,
        'predictions': y_pred_rf,
        'accuracy': accuracy_score(y_test, y_pred_rf),
        'precision': precision_score(y_test, y_pred_rf, average='weighted'),
        'recall': recall_score(y_test, y_pred_rf, average='weighted'),
        'f1': f1_score(y_test, y_pred_rf, average='weighted')
    }
    
    # Gradient Boosting
    print("Training Gradient Boosting...")
    gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb.fit(X_train, y_train)
    y_pred_gb = gb.predict(X_test)
    results['Gradient Boosting'] = {
        'model': gb,
        'predictions': y_pred_gb,
        'accuracy': accuracy_score(y_test, y_pred_gb),
        'precision': precision_score(y_test, y_pred_gb, average='weighted'),
        'recall': recall_score(y_test, y_pred_gb, average='weighted'),
        'f1': f1_score(y_test, y_pred_gb, average='weighted')
    }
    
    return results, y_test

def plot_category_distribution(df):
    """Plot news category distribution"""
    category_counts = df['category'].value_counts()
    
    plt.figure(figsize=(10, 6))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    plt.bar(category_counts.index, category_counts.values, color=colors, edgecolor='black', alpha=0.7)
    plt.xlabel('News Category', fontsize=12)
    plt.ylabel('Number of Articles', fontsize=12)
    plt.title('Distribution of News Articles by Category', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/category_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Category distribution plot saved")

def plot_model_comparison(results):
    """Compare model performance"""
    models = list(results.keys())
    accuracy_scores = [results[m]['accuracy'] for m in models]
    precision_scores = [results[m]['precision'] for m in models]
    recall_scores = [results[m]['recall'] for m in models]
    f1_scores = [results[m]['f1'] for m in models]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].bar(models, accuracy_scores, color=['#1f77b4', '#ff7f0e', '#2ca02c'], alpha=0.7, edgecolor='black')
    axes[0, 0].set_ylabel('Accuracy', fontsize=11)
    axes[0, 0].set_title('Accuracy Comparison', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylim([0, 1])
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    axes[0, 1].bar(models, precision_scores, color=['#1f77b4', '#ff7f0e', '#2ca02c'], alpha=0.7, edgecolor='black')
    axes[0, 1].set_ylabel('Precision', fontsize=11)
    axes[0, 1].set_title('Precision Comparison', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylim([0, 1])
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    axes[1, 0].bar(models, recall_scores, color=['#1f77b4', '#ff7f0e', '#2ca02c'], alpha=0.7, edgecolor='black')
    axes[1, 0].set_ylabel('Recall', fontsize=11)
    axes[1, 0].set_title('Recall Comparison', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylim([0, 1])
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    axes[1, 1].bar(models, f1_scores, color=['#1f77b4', '#ff7f0e', '#2ca02c'], alpha=0.7, edgecolor='black')
    axes[1, 1].set_ylabel('F1-Score', fontsize=11)
    axes[1, 1].set_title('F1-Score Comparison', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylim([0, 1])
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Model comparison plot saved")

def plot_confusion_matrix(results, y_test, label_encoder):
    """Plot confusion matrices for best model"""
    best_model_name = max(results, key=lambda x: results[x]['accuracy'])
    y_pred = results[best_model_name]['predictions']
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(10, 8))
    categories = label_encoder.classes_
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=categories, yticklabels=categories, cbar_kws={'label': 'Count'})
    plt.xlabel('Predicted Category', fontsize=12)
    plt.ylabel('Actual Category', fontsize=12)
    plt.title(f'Confusion Matrix - {best_model_name}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Confusion matrix plot saved")

def plot_classification_metrics(results):
    """Plot classification metrics comparison"""
    models = list(results.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(models))
    width = 0.2
    
    for i, metric in enumerate(metrics):
        values = [results[m][metric] for m in models]
        ax.bar(x + i * width, values, width, label=metric.capitalize(), alpha=0.8)
    
    ax.set_xlabel('Models', fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Classification Metrics Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models)
    ax.legend(fontsize=11)
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/classification_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Classification metrics plot saved")

def plot_category_accuracy(results, y_test, label_encoder):
    """Plot per-category accuracy"""
    best_model_name = max(results, key=lambda x: results[x]['accuracy'])
    y_pred = results[best_model_name]['predictions']
    
    categories = label_encoder.classes_
    category_accuracy = []
    
    for i, category in enumerate(categories):
        mask = y_test == i
        if mask.sum() > 0:
            acc = (y_pred[mask] == y_test[mask]).mean()
            category_accuracy.append(acc)
        else:
            category_accuracy.append(0)
    
    plt.figure(figsize=(10, 6))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    plt.bar(categories, category_accuracy, color=colors, edgecolor='black', alpha=0.7)
    plt.xlabel('News Category', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.title(f'Per-Category Classification Accuracy - {best_model_name}', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.ylim([0, 1])
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/category_accuracy.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Category accuracy plot saved")

def main():
    print("="*80)
    print("NEWS ARTICLE CLASSIFICATION SYSTEM")
    print("="*80)
    
    # Step 1: Generate dataset
    print("\n[Step 1] Generating news dataset...")
    df = generate_news_dataset(1000)
    df.to_csv('/home/ubuntu/news_articles.csv', index=False)
    print(f"✓ Dataset generated: {len(df)} articles, {df['category'].nunique()} categories")
    
    # Step 2: Preprocess data
    print("\n[Step 2] Preprocessing text data...")
    X_train, X_test, y_train, y_test, vectorizer, label_encoder = preprocess_text(df)
    print(f"✓ Data preprocessed: {X_train.shape[0]} training, {X_test.shape[0]} testing")
    
    # Step 3: Train models
    print("\n[Step 3] Training classification models...")
    results, y_test = train_classifiers(X_train, X_test, y_train, y_test)
    
    # Step 4: Evaluate models
    print("\n[Step 4] Evaluating models...")
    print("\nModel Performance:")
    for model_name, result in results.items():
        print(f"\n{model_name}:")
        print(f"  Accuracy:  {result['accuracy']:.4f}")
        print(f"  Precision: {result['precision']:.4f}")
        print(f"  Recall:    {result['recall']:.4f}")
        print(f"  F1-Score:  {result['f1']:.4f}")
    
    # Step 5: Generate visualizations
    print("\n[Step 5] Generating visualizations...")
    plot_category_distribution(df)
    plot_model_comparison(results)
    plot_confusion_matrix(results, y_test, label_encoder)
    plot_classification_metrics(results)
    plot_category_accuracy(results, y_test, label_encoder)
    
    print("\n" + "="*80)
    print("CLASSIFICATION SYSTEM ANALYSIS COMPLETED")
    print("="*80)

if __name__ == "__main__":
    main()
