# ml_utils.py
import joblib
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics.pairwise import cosine_similarity

job_trend_modelzz = joblib.load('report_generator/models/job_posting_trend_model.pkl')
job_recommendation_modelzz = joblib.load('report_generator/models/job_recommendation.pkl')


class JobRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.trend_model = LinearRegression()
        
        # Predefined job titles and descriptions
        self.job_data = {
            "Software Engineer": "Software development programming coding algorithms systems",
            "Data Analyst": "Data analysis statistics visualization reporting SQL",
            "Project Manager": "Project management leadership coordination planning organization",
            "Business Analyst": "Business analysis requirements documentation process improvement",
            "Product Manager": "Product strategy development roadmap user experience",
            "Data Scientist": "Machine learning data science algorithms statistics modeling",
            "UX Designer": "User experience design interface wireframes usability",
            "DevOps Engineer": "Infrastructure deployment automation CI/CD cloud",
            "Marketing Manager": "Marketing strategy campaigns analytics branding",
            "Sales Representative": "Sales business development client relationships negotiation"
        }
        
        # Fit vectorizer with job descriptions
        self.job_descriptions = list(self.job_data.values())
        self.job_titles = list(self.job_data.keys())
        self.vectorizer.fit(self.job_descriptions)
        
        # Pre-compute job vectors
        self.job_vectors = self.vectorizer.transform(self.job_descriptions)
        
        # Initialize trend model with simple data
        # Months as features (1-12)
        X_trend = np.array(range(1, 13)).reshape(-1, 1)
        # Simple synthetic trend data
        y_trend = 100 + 10 * np.sin(X_trend.ravel() * np.pi / 6) + np.random.normal(0, 2, 12)
        self.trend_model.fit(X_trend, y_trend)

def get_job_recommendations(resume_text, num_recommendations=5):
    try:
        recommender = JobRecommender()
        
        if not resume_text:
            return _get_default_recommendations(num_recommendations)

        # Transform resume text
        resume_vector = recommender.vectorizer.transform([resume_text])
        
        # Calculate similarities
        similarities = cosine_similarity(resume_vector, recommender.job_vectors)[0]
        
        # Get top recommendations
        top_indices = np.argsort(similarities)[-num_recommendations:][::-1]
        
        return [
            (recommender.job_titles[idx], float(similarities[idx]))
            for idx in top_indices
        ]
        
    except Exception as e:
        print(f"Error in get_job_recommendations: {str(e)}")
        return _get_default_recommendations(num_recommendations)

def _get_default_recommendations(num_recommendations):
    default_jobs = [
        "Software Engineer",
        "Data Analyst",
        "Project Manager",
        "Business Analyst",
        "Product Manager"
    ]
    return [(job, 0.8) for job in default_jobs[:num_recommendations]]

def analyze_job_market_trends(job_title):
    try:
        recommender = JobRecommender()
        current_date = datetime.now()
        
        # Prepare input features
        X = np.array([[current_date.month]])
        
        # Get prediction
        prediction = recommender.trend_model.predict(X)[0]
        
        return {
            'prediction': float(prediction),
            'month': current_date.month,
            'year': current_date.year,
            'job_title': job_title
        }
        
    except Exception as e:
        print(f"Error in analyze_job_market_trends: {str(e)}")
        return _get_default_trend_analysis(job_title)

def _get_default_trend_analysis(job_title):
    current_date = datetime.now()
    return {
        'prediction': 0,
        'month': current_date.month,
        'year': current_date.year,
        'job_title': job_title,
        'error': 'Could not generate accurate trend prediction'
    }

