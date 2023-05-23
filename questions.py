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
def ask_experience():
    while True:
        user_input = input("Do you have any previous working experience in Data/IT? (yes/no): ").lower()
        if user_input == "yes":
            return True
        elif user_input == "no":
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Question 3: What type of programming are you interested in?
def ask_programming_type():
    programming_types = {
        1: "General-Purpose Programming",
        2: "Web Development",
        3: "Databases and Data Manipulation",
        4: "Scientific and Mathematical Computing",
        5: "Not interested in programming"
    }

    print("Programming Types:")
    for i, programming_type in programming_types.items():
        print(f"{i}. {programming_type}")

    while True:
        print("Enter the number(s) corresponding to your choice(s). Separate multiple choices by commas.")
        user_input = input("Your choice(s): ").lower()

        selected_types = []
        selected_indexes = user_input.split(",")
        selected_types = [programming_types[int(index.strip())] for index in selected_indexes if index.strip().isdigit()]

        print("Selected programming type(s):")
        for programming_type in selected_types:
            print(programming_type)

        confirm = input("Are these your final selections? (yes/no): ").lower()
        if confirm == "yes":
            break

    print("Final selected programming type(s):")
    for programming_type in selected_types:
        print(programming_type)

    return selected_types

# Question 4: Select specific programming languages that you would like to work with
def ask_specific_languages(programming_types):
    specific_languages = []

    for programming_type in programming_types:
        if programming_type == "Not interested in programming":
            break
        elif programming_type == "General-Purpose Programming":
            general_purpose_languages = ["Java", "Python", "C#", "TypeScript", "JavaScript", "C++", "Go", "C"]
            specific_languages.extend(general_purpose_languages)
        elif programming_type == "Web Development":
            web_dev_languages = ["CSS", "HTML", "PHP"]
            specific_languages.extend(web_dev_languages)
        elif programming_type == "Databases and Data Manipulation":
            specific_languages.append("SQL")
        elif programming_type == "Scientific and Mathematical Computing":
            sci_math_languages = ["MATLAB", "R"]
            specific_languages.extend(sci_math_languages)

    if specific_languages:
        print("Specific programming languages:")
        for i, language in enumerate(specific_languages, start=1):
            print(f"{i}. {language}")
        while True:
            print("Enter the number(s) corresponding to your choice(s). Separate multiple choices by commas.")
            user_input = input("Your choice(s): ").lower()
            selected_indexes = user_input.split(",")
            selected_languages = [specific_languages[int(index.strip()) - 1] for index in selected_indexes if index.strip().isdigit()]
            if selected_languages:
                break
            else:
                print("Invalid input. Please enter the number(s) corresponding to your choice(s).")

        print("Selected programming language(s):")
        for language in selected_languages:
            print(language)
        
        return selected_languages
    else:
        print("No specific programming languages selected.")
        return specific_languages

# Additional questions...
# ...

# Analyze the user's responses and make recommendations based on the data
#def analyze_responses(selected_occupation_groups, experience, programming_languages):
    # Implement the code for analysis and recommendations using the data analysis functions from data_analyzer.py
    # ...
