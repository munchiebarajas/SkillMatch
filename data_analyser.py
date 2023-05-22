import pandas as pd
import re

data = pd.read_csv('jobtech_2023clean.csv')
#Check how many total vacancies there is of the occupations
def totalvacancies(data, n=10):
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
        print(f"{value}: {count}")

#Check for string in column
def get_string(data, column_name, search_string):
    filtered_data = data[data[column_name].notna() & data[column_name].str.contains(search_string, case=False, na=False)]
    print(f"Filtered values in column '{column_name}' containing '{search_string}':")
    for value in filtered_data[column_name].unique():
        print(value)

#Check for string in column, count occurances
def count_string_occ(data, column_name, search_string):
    pattern = fr"(?i)(?<!\S){re.escape(search_string)}(?!\S)"
    filtered_data = data[data[column_name].notna() & data[column_name].str.contains(pattern, regex=True)]
    count = filtered_data[column_name].str.contains(pattern, regex=True).sum()
    print(f"Number of occurrences of '{search_string}' in column '{column_name}': {count}")

search_string = 'c#'
column_name = 'annonstext'
#get_col_values(data, column_name)
count_string_occ(data, column_name, search_string)