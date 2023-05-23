import pandas as pd
import numpy as np
import re

from data_analyzer import count_job_postings

data = pd.read_csv('jobtech_2023clean.csv')
# Question 1: Choose the occupation groups that interest you
def get_selected_occupation_groups():
    occupation_counts = data['occupation_group_name'].value_counts()
    occupations = list(occupation_counts.index)

    print("Occupation groups:")
    for i, occupation in enumerate(occupations, start=1):
        print(f"{i}. {occupation}")

    while True:
        print("Enter the number(s) corresponding to your choice(s). Separate multiple choices by commas.")
        print("Enter 'any' to select all occupation groups.")

        user_input = input("Your choice(s): ").lower()

        if user_input == "any":
            selected_occupations = occupations
        else:
            selected_indexes = user_input.split(",")
            selected_occupations = [occupations[int(index.strip()) - 1] for index in selected_indexes if index.strip().isdigit()]

        print("Selected occupation group(s):")
        for occupation in selected_occupations:
            print(occupation)

        confirm = input("Are these your final selections? (yes/no): ").lower()
        if confirm == "yes":
            break

    print("Final selected occupation group(s):")
    for occupation in selected_occupations:
        print(occupation)

    return selected_occupations

# Question 2: Do you have any previous working experience in Data/IT?
#def ask_experience():
    # Implement the code for this question
    # ...

# Question 3: Do you like programming? If yes, choose languages that you are familiar with and would like to work with.
#def ask_programming_languages():
    # Implement the code for this question
    # ...

# Additional questions...
# ...

# Analyze the user's responses and make recommendations based on the data
#def analyze_responses(selected_occupation_groups, experience, programming_languages):
    # Implement the code for analysis and recommendations using the data analysis functions from data_analyzer.py
    # ...
