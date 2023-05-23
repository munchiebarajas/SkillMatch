import pandas as pd
import re

data = pd.read_csv('jobtech_2023clean.csv')

#Check number of job postings (not vacancies) returns count
def count_job_postings(data, occupation):
    total_count = len(data[data['occupation'] == occupation])
    return total_count

#Check how many total vacancies there is of the occupations
def total_vac(data, n=10):
    occupation_counts = data['occupation'].value_counts()
    print("Vacancies for each occupation:")
    # Get the top n occupations with the highest number of vacancies
    top_occupations = occupation_counts.head(n)

    for occupation, count in top_occupations.items():
        # Filter the data for the current occupation
        occupation_data = data[data['occupation'] == occupation]

        # Calculate the total number of vacancies for the current occupation
        total_vacancies = occupation_data['number_of_vacancies'].sum()

        print(f"{occupation}", ":", f"{total_vacancies}")

#Check what distinct values there are in a column
def get_col_values(data, column_name):
    value_counts = data[column_name].value_counts()
    print(f"Distinct values in column '{column_name}':")
    for value, count in value_counts.items():
        print(f"{value}")#: {count}")

#Check for string in column
def get_str(data, column_name, search_string):
    filtered_data = data[data[column_name].notna() & data[column_name].str.contains(search_string, case=False, na=False)]
    print(f"Filtered values in column '{column_name}' containing '{search_string}':")
    for value in filtered_data[column_name].unique():
        print(value)

#Check for string in column, count occurances. Returns count, so call print(count_str(data, column_name, search_string)) to print the count
def count_str(data, column_name, search_string):
    pattern = fr"(?i)(?<!\S){re.escape(search_string)}(?!\S)"
    filtered_data = data[data[column_name].notna() & data[column_name].str.contains(pattern, regex=True)]
    count = filtered_data[column_name].str.contains(pattern, regex=True).sum()
    return count

#Check how many times a string occurs in 'annonstext' for each occupation, prints the top x
def count_str_per_job(data, search_string, top_n=5):
    occupation_occurrences = {}

    # Iterate over each occupation
    for occupation in data['occupation'].unique():
        # Filter the data for the current occupation
        occupation_data = data[data['occupation'] == occupation]

        # Count the occurrences of the search string using the count_str function
        count = count_str(occupation_data, 'annonstext', search_string)

        # Store the occupation and count in the dictionary
        occupation_occurrences[occupation] = count

    # Sort the dictionary by values in descending order
    sorted_occurrences = sorted(occupation_occurrences.items(), key=lambda x: x[1], reverse=True)

    print(f"Top {top_n} occupations with the most occurrences of '{search_string}':")
    for i, (occupation, count) in enumerate(sorted_occurrences[:top_n], 1):
        print(f"{i}. Occupation: {occupation}")
        print(f"   Occurrences: {count}")

#Counts how many times each of the skills occur in the 'annonstext'
def count_skills_per_job(data):
    skill_occurrences = {}

    # Iterate over each skill value in the 'required_skills' column
    for value in data['required_skills'].dropna().unique():
        # Extract the skill name (before the comma, if present)
        skill_name = re.match(r'^([^,]+)(?:,|$)', value.strip()).group(1)

        # Count the occurrences of the skill name in the 'annonstext' column
        count = count_str(data, 'annonstext', skill_name)

        # Store the skill and count in the dictionary
        skill_occurrences[skill_name] = count

    # Sort the dictionary by values in descending order
    sorted_occurrences = sorted(skill_occurrences.items(), key=lambda x: x[1], reverse=True)

    # Print the list of skills and their occurrences
    print("Skills and their occurrences:")
    for i, (skill, count) in enumerate(sorted_occurrences, 1):
        print(f"{i}. Skill: {skill}")
        print(f"   Occurrences: {count}")

def count_str_percentage_per_job(data, search_string, top_n=5, min_postings=0):
    occupation_occurrences = {}

    # Iterate over each occupation
    for occupation in data['occupation'].unique():
        # Filter the data for the current occupation
        occupation_data = data[data['occupation'] == occupation]

        # Count the total number of job postings for the current occupation
        job_postings_count = len(occupation_data)

        # Skip occupations with total postings below the minimum threshold
        if job_postings_count < min_postings:
            continue

        # Count the occurrences of the search string in the 'annonstext' column
        count = count_str(occupation_data, 'annonstext', search_string)

        # Calculate the percentage of occurrences relative to the total job postings
        percentage = (count / job_postings_count) * 100

        # Store the occupation, count, and percentage in the dictionary
        occupation_occurrences[occupation] = {'count': job_postings_count, 'percentage': percentage}

    # Sort the dictionary by percentage values in descending order
    sorted_occurrences = sorted(occupation_occurrences.items(), key=lambda x: x[1]['percentage'], reverse=True)

    print(f"Top {top_n} occupations with the highest percentage of occurrences for '{search_string}':")
    for i, (occupation, data) in enumerate(sorted_occurrences[:top_n], 1):
        count = data['count']
        percentage = data['percentage']
        print(f"{i}. Occupation: {occupation}")
        print(f"   {percentage:.2f}% of {count} postings")


search_string = 'python'
column_name = 'required_skills'
occupation = 'Backend-utvecklare'
#count_skills_per_job(data)

#get_col_values(data, column_name)
#total_vac(data)
#print(count_job_postings(data, occupation))
#print(count_str(data, column_name, search_string))
count_str_percentage_per_job(data, search_string, top_n=5, min_postings = 100)
