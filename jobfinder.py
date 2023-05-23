import pandas as pd
import numpy as np

from questions import get_selected_occupation_groups, ask_experience, ask_programming_type, ask_specific_languages#, analyze_responses

# Question 1: Choose the occupation groups that interest you
selected_occupation_groups = get_selected_occupation_groups()

# Question 2: Do you have any previous working experience in Data/IT?
experience = ask_experience()

# Question 3: Do you like programming? If so, what kind of programming interests you?
programming_type = ask_programming_type()

# Question 4: Are in interested in any specific programming languages?
specific_languages= ask_specific_languages(programming_type)


# Analyze the user's responses and make recommendations based on the data
#analyze_responses(selected_occupation_groups, experience, programming_languages)