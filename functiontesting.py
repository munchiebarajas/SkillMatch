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

# Preset user inputs (for testing and development)
selected_occupation_groups = ['Mjukvaru- och systemutvecklare m.fl.', 'Systemförvaltare m.fl.']
experience = [1,2]
programming_type = ['General-Purpose Programming', 'Web Development']
specific_languages = ['Python', 'CSS', 'C#']


data = pd.read_csv('jobtech_2023clean.csv')

recommendation = Recommendation(data, selected_occupation_groups, experience, programming_type, specific_languages, question_weights, answer_weights)
#user_preferences = recommendation.calculate_user_preferences()
#print(json.dumps(user_preferences, indent=4, ensure_ascii=False))
occupation_profiles = recommendation.compute_occupation_profiles()
# Print the first two entries
count = 0
for occupation, profile in occupation_profiles.items():
    print(occupation, ":", profile)
    count += 1
    if count == 2:
        break
