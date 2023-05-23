import pandas as pd
import numpy as np

from questions import ask_occupation_groups, ask_experience, ask_programming_languages, analyze_responses

# Question 1: Choose the occupation groups that interest you
selected_occupation_groups = ask_occupation_groups()

# Question 2: Do you have any previous working experience in Data/IT?
experience = ask_experience()

# Question 3: Do you like programming? If yes, choose languages that you are familiar with and would like to work with.
programming_languages = ask_programming_languages()

# Analyze the user's responses and make recommendations based on the data
analyze_responses(selected_occupation_groups, experience, programming_languages)