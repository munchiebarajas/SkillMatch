import pandas as pd
import re
import csv
from collections import Counter

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
        print(f"{value}",":", f"{count}")

#Check for string in column
def get_str(data, column_name, search_string):
    filtered_data = data[data[column_name].notna() & data[column_name].str.contains(search_string, case=False, na=False)]
    print(f"Filtered values in column '{column_name}' containing '{search_string}':")
    for value in filtered_data[column_name].unique():
        print(value)

#Check for string in column, count occurances. Returns count, so call print(count_str(data, column_name, search_string)) to print the count.
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
#Count how many times each skill is mentioned in the annonstext column (once per entry)
def count_skills_in_annonstext(data, additional_skills=None):
    skill_occurrences = {}

    # Iterate over each annonstext
    for annonstext in data['annonstext'].dropna().unique():
        # Initialize a set to store unique skills in the annonstext
        unique_skills = set()

        # Iterate over each skill value in the 'required_skills' column
        for value in data['required_skills'].dropna().unique():
            # Extract the skill name (before the comma, if present)
            skill_name = re.match(r'^([^,]+)(?:,|$)', value.strip()).group(1)

            # Check if the skill is present in the current annonstext
            if skill_name.lower() in annonstext.lower():
                # Add the skill to the set of unique skills
                unique_skills.add(skill_name)

        # Add manually specified additional skills to the set of unique skills
        if additional_skills:
            for skill in additional_skills:
                if skill.lower() in annonstext.lower():
                    unique_skills.add(skill)

        # Update the skill occurrences dictionary
        for skill in unique_skills:
            skill_occurrences[skill] = skill_occurrences.get(skill, 0) + 1

    # Sort the dictionary by values in descending order
    sorted_occurrences = sorted(skill_occurrences.items(), key=lambda x: x[1], reverse=True)

    # Print the list of skills and their occurrences
    print("Skills and their occurrences:")
    for i, (skill, count) in enumerate(sorted_occurrences, 1):
        print(f"{i}. Skill: {skill}")
        print(f"   Occurrences: {count}")
#Same as above but saves result to csv
def count_skills_in_annonstext_csv(data, additional_skills=None, output_file='skill_occurrences.csv'):
    skill_occurrences = {}

    # Iterate over each skill value in the 'required_skills' column
    for value in data['required_skills'].dropna().unique():
        # Extract the skill name (before the comma, if present)
        skill_name = re.match(r'^([^,]+)(?:,|$)', value.strip()).group(1)

        # Count the occurrences of the skill name in the 'annonstext' column
        count = count_str(data, 'annonstext', skill_name)

        # Store the skill and count in the dictionary
        skill_occurrences[skill_name] = count

    # Add manually specified additional skills to the dictionary
    if additional_skills:
        for skill in additional_skills:
            count = count_str(data, 'annonstext', skill)
            skill_occurrences[skill] = count

    # Sort the dictionary by values in descending order
    sorted_occurrences = sorted(skill_occurrences.items(), key=lambda x: x[1], reverse=True)

    # Save the skill occurrences to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Skill', 'Occurrences'])
        writer.writerows(sorted_occurrences)

    print(f"Skill occurrences saved to '{output_file}' file.")

#Count occurance of programspråk in annonstext
def count_progsprak_in_annonstext(data):
    skill_occurrences = {}

    # Iterate over each skill value in the 'required_skills' column
    for value in data['required_skills'].dropna().unique():
        # Check if the skill value contains the phrase 'programmeringsspråk'
        if 'programmeringsspråk' in value.lower():
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

#Counts percentage of occupation postings that contain string
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

#Counts how often a list of strings is found in annonstext
def count_newlang_in_annonstext(data, languages):
    skill_occurrences = {}

    # Iterate over each language in the list
    for language in languages:
        # Count the occurrences of the language in the 'annonstext' column
        count = count_str(data, 'annonstext', language)

        # Store the language and count in the dictionary
        skill_occurrences[language] = count

    # Sort the dictionary by values in descending order
    sorted_occurrences = sorted(skill_occurrences.items(), key=lambda x: x[1], reverse=True)

    # Print the list of languages and their occurrences
    print("Languages and their occurrences:")
    for i, (language, count) in enumerate(sorted_occurrences, 1):
        print(f"{i}. Language: {language}")
        print(f"   Occurrences: {count}")

#Counts the most common words in a column
def count_common_words(data, column_name, skip_n, top_n):
    word_counts = Counter()

    # Iterate over each value in the specified column
    for value in data[column_name].dropna():
        # Extract words from the value using regex
        words = re.findall(r'\b\w+\b', value.lower())

        # Update word counts, excluding words with fewer than 4 characters
        word_counts.update(word for word in words if len(word) >= 4)

    # Get the most common words
    most_common_words = word_counts.most_common(skip_n + top_n)

    # Skip the top N words
    skipped_words = most_common_words[skip_n:]

    # Print the skipped words and their frequencies
    print(f"Skipped {skip_n} common words (with at least 4 characters) in column '{column_name}':")
    for i, (word, count) in enumerate(skipped_words, start=1):
        print(f"{i}. Word: {word}")
        print(f"   Frequency: {count}")

def percentage_of_values_per_occupation(data, column_name):
    occupation_analysis = {}

    # Iterate over each occupation
    for occupation in data['occupation'].unique():
        # Filter the data for the current occupation
        occupation_data = data[data['occupation'] == occupation]

        # Calculate the percentage of each value in the specified column
        value_counts = occupation_data[column_name].value_counts(normalize=True) * 100

        # Store the occupation and value counts in the dictionary
        occupation_analysis[occupation] = value_counts

    # Print the analysis results
    for occupation, analysis in occupation_analysis.items():
        print(f"Occupation: {occupation}")
        print(analysis)
        print('\n')

languages = [
    'Java',
    'Python',
    'SQL',
    'C#',
    'JavaScript',
    'C++',
    'C',
    'HTML',
    'PHP',
    'Erlang',
    'Java Enterprise Edition',
    'Java Standard Edition',
    'CSS',
    'Ruby',
    'Swift',
    'Go',
    'Rust',
    'TypeScript',
    'Kotlin',
    'Perl',
    'Shell scripting (e.g., Bash)',
    'MATLAB',
    'R'
]

additional_skills = ['']
search_string = 'tensorflow'
column_name = 'occupation'
occupation = 'Backend-utvecklare'
#print (data.columns)
get_col_values(data, column_name)
#get_str(data,column_name,search_string)
#total_vac(data)
#print(count_job_postings(data, occupation))
print(count_str(data, column_name, search_string))
#count_str_per_job(data, search_string, top_n=5)
#count_str_percentage_per_job(data, search_string, top_n=5, min_postings=50)
#count_skills_in_annonstext(data)
#count_progsprak_in_annonstext(data)
#count_newlang_in_annonstext(data, languages)
#count_common_words(data, column_name, 0, 20)
#count_skills_in_annonstext_csv(data, additional_skills, )
#percentage_of_values_per_occupation(data, column_name)