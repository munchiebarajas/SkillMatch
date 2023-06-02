import json
import pandas as pd
from recommendation_engine import RecommendationEngine

# Load data and profiles
data = pd.read_csv('jobtech_2023clean.csv')
profiles = pd.read_csv('occupation_profiles.csv')
print(data.head())  # Display the first few rows of the data dataframe
print(profiles.head())  # Display the first few rows of the profiles dataframe
# Create recommendation engine
engine = RecommendationEngine(data, profiles)

# Create recommendation
recommendation = engine.create_recommendation()
user_preferences = recommendation.calculate_user_preferences()
#print (user_preferences)
similarities = recommendation.measure_similarity(user_preferences, profiles)

ranked_occupations = recommendation.rank_occupations(similarities)
top_recommendations = recommendation.get_top_n_recommendations(ranked_occupations, similarities, 10)

# Print top recommendations
for occupation, rating in top_recommendations:
    print(f"Occupation: {occupation}, Rating: {rating}")
