import pandas as pd
import numpy as np
import re


data = pd.read_csv('jobtech_2023clean.csv')

pattern_list = ['års erfarenhet', 'år erfarenhet', 'år av erfarenhet', 'år arbetserfarenhet', 'års arbetserfarenhet', 'år av arbetserfarenhet', 'års arbetslivserfarenhet',
                'år arbetslivserfarenhet', 'år av arbetslivserfarenhet', 'years of experience', 'year of experience', 'års relevant arbetserfarenhet', 'år relevant arbetserfarenhet',
                'år av relevant arbetserfarenhet', 'år av relevant arbetslivserfarenhet', 'års relevant arbetslivserfarenhet', 'år relevant arbetslivserfarenhet',
                'experience', 'years experience', 'years of relevant experience', 'year of relevant experience', 'years relevant experience', 'years of work experience',
                'year of work experience', 'years work experience', 'years of relevant work experience', 'year of relevant work experience', 'years relevant work experience',
                ]
preceding_words = ['fem', 'five', 'fyra', 'four', 'tre', 'three', 'två', 'two', 'ett', 'one', 'några', 'någon', 'some', 'few']
weight_mapping = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'ett': 1,
    'två': 2,
    'tre': 3,
    'fyra': 4,
    'fem': 5,
    'några': 2,
    'någon': 1,
    'some': 2,
    'few': 2
}

#Function to get the % where experience_required is True for each occupation
def compute_proportion_experience_required(occupation):
    total_entries = len(data[data['occupation'] == occupation])
    if total_entries == 0:
        return 0.0
    experience_required_entries = len(data[(data['occupation'] == occupation) & (data['experience_required'])])
    proportion_experience_required = experience_required_entries / total_entries
    return proportion_experience_required

def count_exp_str(data, column_name, pattern_list, preceding_words):
    count = 0
    match_count = 0
    for pattern in pattern_list:
        for preceding_word in preceding_words:
            lowercase_preceding_word = preceding_word.lower()
            if lowercase_preceding_word in weight_mapping:
                weight = weight_mapping[lowercase_preceding_word]
                pattern_regex = fr"(?i)(?<!\S){re.escape(preceding_word)}\s*(?:\d+\s*)?{re.escape(pattern)}(?!\S)"
                matches = data[column_name].str.findall(pattern_regex, flags=re.IGNORECASE)
                count += sum(len(match) * weight for match in matches if isinstance(match, list))
                match_count += sum(1 for match in matches if isinstance(match, list) and len(match) > 0)
    if match_count > 0:
        count /= match_count
    return count

def compute_exp_word_counts(data, occupation, pattern_list, preceding_words):
    occupation_data = data[data['occupation'] == occupation]
    count = count_exp_str(occupation_data, 'annonstext', pattern_list, preceding_words)
    proportion = compute_proportion_experience_required(occupation)
    count *= proportion
    return count

def count_str(data, column_name, search_string):
    pattern = fr"(?i)(?<!\S){re.escape(search_string)}(?!\S)"
    filtered_data = data[data[column_name].notna() & data[column_name].str.contains(pattern, regex=True)]
    count = filtered_data[column_name].str.contains(pattern, regex=True).sum()
    return count

def compute_not_interested_programming_score(data, occupation, word_list):
    occupation_data = data[data['occupation'] == occupation]
    job_postings = len(occupation_data)
    count = 0
    for index, row in occupation_data.iterrows():
        posting_text = row['annonstext']
        if isinstance(posting_text, str):  # Check if posting_text is a string
            words_found = any(word in posting_text.lower() for word in word_list)
        else:
            words_found = False
        if not words_found:
            count += 1
    score = count / job_postings
    return score

# Check how well each occupation matches with the programming types
def compute_word_counts(data, occupation, word_list):
    occupation_data = data[data['occupation'] == occupation]
    count = 0
    for word in word_list:
        count += count_str(occupation_data, 'annonstext', word)
    return count

def compute_sp_word_counts(data, occupation, word_list):
    occupation_data = data[data['occupation'] == occupation]
    counts = {}
    for word in word_list:
        counts[word] = count_str(occupation_data, 'annonstext', word)
    return counts

# Word lists for matching
web_development_words = ['html','css','javascript','front-end','frontend','user interface','ui','user experience','ux','användarupplevelse','design','web','website','hemsida','web application','web applications','seo','e-commerce','wordpress','google','Facebook']
general_purpose_programming_words = ['java', 'python', 'c++', 'ruby', 'Software development', 'mjukvaruutveckling', 'problem solving', 'problemlösning', 'Version control', 'ui', 'ux', 'ai', 'programming', 'coding', 'software', 'development']
databases_data_manipulation_words = ['sql', 'database', 'query', 'data', 'update', 'uppdatera','databas', 'Data analysis', 'datanalys', 'ETL' ]
scientific_mathematical_computing_words = ['math', 'statistics', 'simulation', 'AI', 'Artificial intelligence', 'Machine Learning', 'Algorithm', 'Algoritm', 'statistik', 'Analysis', 'Analys', 'Matematik', 'matte', 'Experiment', 'Algebra', 'Research', 'Matrix', 'Probability', 'sannolikhet', 'theory', 'teori']
not_interested_programming_words = ['javascript', 'utvecklare', 'programming', 'programmera', 'programmering', 'coding', 'software', 'development', 'java', 'python', 'c++', 'c#', 'ruby', 'software development', 'mjukvaruutveckling', 'ui', 'ux']
product_owner_words = ['team', 'lag', 'teamleader', 'ledare', 'lagledare', 'teambuilding', 'kollegor', 'kommunikation', 'produktägare', 'product owner', 'project', 'projekt', 'project leader', 'projektledare']
specific_languages = ["Java", "Python", "C#", "TypeScript", "JavaScript", "C++", "Go", "C", "CSS", "HTML", "PHP", "MATLAB", "R", "SQL", "NoSQL", "SQLite"]



# Creates a dictionary of occupation profiles, storing their values which will be used for matching.
def compute_occupation_profiles():
    # Creates an entry for each occupation and calls the appropriate functions for them
    occupation_profiles = {}
    for occupation in data['occupation']:
        if occupation not in occupation_profiles:
            occupation_entries = len(data[data['occupation'] == occupation])
            profile = {
                'occupation_group_name': data.loc[data['occupation'] == occupation, 'occupation_group_name'].values[0],
                'Experience': compute_exp_word_counts(data, occupation, pattern_list, preceding_words),
                'Web Development': compute_word_counts(data, occupation, web_development_words) / occupation_entries,
                'General-Purpose Programming': compute_word_counts(data, occupation, general_purpose_programming_words) / occupation_entries,
                'Databases and Data Manipulation': compute_word_counts(data, occupation, databases_data_manipulation_words) / occupation_entries,
                'Scientific and Mathematical Computing': compute_word_counts(data, occupation, scientific_mathematical_computing_words) / occupation_entries,
                'Not interested in programming': compute_not_interested_programming_score(data, occupation, not_interested_programming_words),
                'Product Owner': compute_word_counts(data, occupation, product_owner_words) / occupation_entries
            }
            
            specific_languages_count = compute_sp_word_counts(data, occupation, specific_languages)
            for language in specific_languages:
                profile[language] = specific_languages_count.get(language, 0) / occupation_entries
            

            occupation_profiles[occupation] = profile

    return occupation_profiles

Profiles = compute_occupation_profiles()
# Convert the occupation profiles dictionary to a DataFrame
df_profiles = pd.DataFrame.from_dict(Profiles, orient='index')

# Set the index name
df_profiles.index.name = 'Occupation'

# Save the DataFrame to a CSV file
df_profiles.to_csv('occupation_profiles.csv')
