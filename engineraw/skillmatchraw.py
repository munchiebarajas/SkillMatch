import pandas as pd
import numpy as np
import re
import json
from recommendation_engineraw import RecommendationEngine

profiles = pd.read_csv('occupation_profiles.csv')
data = pd.read_csv('jobtech_2023clean.csv')
recommendation_engine = RecommendationEngine(data, profiles)
recommendation = recommendation_engine.create_recommendation()
recommend_occupations = recommendation.run()
# Print the top matches with scores

print("Top Recommendations:")
for occupation, rating in recommend_occupations:
    formatted_rating = "{:.2f}".format(rating)  # Limit rating to 2 decimal places
    print(f"{occupation}: {formatted_rating}")
