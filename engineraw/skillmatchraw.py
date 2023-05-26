import pandas as pd
import numpy as np
import re
import json
from recommendation_engineraw import RecommendationEngine, Recommendation

data = pd.read_csv('jobtech_2023clean.csv')
recommendation_engine = RecommendationEngine(data)
recommendation = recommendation_engine.create_recommendation()
recommendations = recommendation.run()
# Print the top matches with scores

print("Top Recommendations:")
for occupation, rating in recommendations:
    formatted_rating = "{:.2f}".format(rating)  # Limit rating to 2 decimal places
    print(f"{occupation}: {formatted_rating}")
