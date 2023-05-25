import pandas as pd
import numpy as np
import re
import json
from recommendation_engine import Recommendation
# Load question weights and answer weights from weight_settings.json
with open('weight_settings.json', 'r') as file:
    weight_settings = json.load(file)

# Extract the question weights and answer weights from the loaded JSON data
question_weights = weight_settings.get('question_weights', {})
answer_weights = weight_settings.get('answer_weights', {})
similarity_weights = weight_settings.get('similarity_weights', {})
# Preset user inputs (for testing and development)
selected_occupation_groups = ['']
experience = [1,2]
programming_type = ['General-Purpose Programming', 'Web Development']
specific_languages = ['frontend']


data = pd.read_csv('jobtech_2023clean.csv')

recommendation = Recommendation(data, selected_occupation_groups, experience, programming_type, specific_languages, question_weights, answer_weights, similarity_weights)
user_preferences = recommendation.calculate_user_preferences()
print(json.dumps(user_preferences, indent=4, ensure_ascii=False))
occupation_profiles = recommendation.compute_occupation_profiles()
# Print the first entry
"""if occupation_profiles:
    profile = next(iter(occupation_profiles))
    contents = occupation_profiles[profile]
    print("Profile:", profile)
    print("Recommendation rating:", contents)
else:
    print("No occupation profiles found.")
"""
match_rating = recommendation.measure_similarity(user_preferences,occupation_profiles)
"""
if match_rating:
    rating = next(iter(match_rating))
    contents = match_rating[rating]
    print("Profile:", rating)
    print("Contents:", contents)
else:
    print("No occupation profiles found.")
"""
rank_occupations = recommendation.rank_occupations(match_rating)
top_matches = recommendation.get_top_n_recommendations(rank_occupations, 10)

# Print the top matches with scores
print("Top Matches:")
for occupation in top_matches:
    score = match_rating[occupation]
    print(f"Occupation: {occupation}, Score: {score}")