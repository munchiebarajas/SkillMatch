import pandas as pd
import numpy as np

data = pd.read_csv('jobtech_2023clean.csv')

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
