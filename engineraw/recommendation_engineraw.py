import json
import re
import pandas as pd
import numpy as np
from questionsraw import get_selected_occupation_groups, ask_experience, ask_programming_type, ask_specific_languages

class RecommendationEngine:
    def __init__(self, data):
        self.data = data

    def create_recommendation(self):
        # Load question and answer weights from the JSON file
        with open('weight_settingsraw.json') as file:
            weight_settings = json.load(file)

        question_weights = weight_settings['question_weights']
        answer_weights = weight_settings['answer_weights']
        similarity_weights = weight_settings['similarity_weights']

        selected_occupation_groups = get_selected_occupation_groups()
        experience = ask_experience()
        programming_type = ask_programming_type()
        specific_languages = ask_specific_languages(programming_type)
        
        # Create recommendation object
        recommendation = Recommendation(
            self.data,
            selected_occupation_groups,
            experience,
            programming_type,
            specific_languages,
            question_weights,
            answer_weights,
            similarity_weights
        )

        return recommendation

class Recommendation:
    def __init__(self, data, selected_occupation_groups, experience, programming_type, specific_languages,
                 question_weights, answer_weights, similarity_weights):
        self.data = data
        self.selected_occupation_groups = selected_occupation_groups
        self.experience = experience
        self.programming_type = programming_type
        self.specific_languages = specific_languages
        self.question_weights = question_weights
        self.answer_weights = answer_weights
        self.similarity_weights = similarity_weights

    def run(self):
        # Step 4: Perform recommendation algorithm

        # Step 4.1: Preprocess the data
        # ...

        # Step 4.2: Define similarity measures
        # ...

        # Step 4.3: Calculate user preferences
        user_preferences = self.calculate_user_preferences()

        # Step 4.4: Compute occupation profiles
        occupation_profiles = self.compute_occupation_profiles()

        # Step 4.5: Measure similarity
        similarity_scores = self.measure_similarity(user_preferences, occupation_profiles)

        # Step 4.6: Rank occupations
        ranked_occupations = self.rank_occupations(similarity_scores)

        # Step 4.7: Return recommended occupations
        recommended_occupations = self.get_top_n_recommendations(ranked_occupations, similarity_scores, n=5)
        return recommended_occupations

    def calculate_user_preferences(self):
        # Calculate occupation group preferences based on selected occupation groups
        occupation_group_preferences = {
            group: self.question_weights['occupation_groups']
            if group in self.selected_occupation_groups else 0.0
            for group in set(self.data['occupation_group_name'])
        }

        # Calculate experience preferences based on work experience and education experience
        work_experience_weight = self.answer_weights.get("experience", {}).get("work_experience", 0.0)
        education_experience_weight = self.answer_weights.get("experience", {}).get("education_experience", 0.0)

        max_experience_rating = 5  # Maximum rating value for both work and education experience

        normalized_work_experience = self.experience[0] / max_experience_rating
        normalized_education_experience = self.experience[1] / max_experience_rating

        experience_preferences = {
            "total_experience": (normalized_work_experience * work_experience_weight) + (normalized_education_experience * education_experience_weight)
        }
        # Add programming type preferences with weights
        programming_type_preferences = {
            programming_type: self.programming_type.count(programming_type) * self.answer_weights.get("programming_type", {}).get("selected_types", 0.0)
            for programming_type in self.programming_type
        }
        # Add specific language preferences with weights
        specific_language_preferences = {
            language: self.specific_languages.count(language) * self.answer_weights.get("specific_languages", {}).get("selected_languages", 0.0)
            for language in self.specific_languages
        }

        # Combine occupation group preferences and experience preferences
        user_preferences = {}
        user_preferences.update(occupation_group_preferences)
        user_preferences.update(experience_preferences)
        user_preferences.update(programming_type_preferences)
        user_preferences.update(specific_language_preferences)

        return user_preferences
    
    #Creates a dictionary of occupation profiles, storing their values which will be used for matching.
    def compute_occupation_profiles(self):
        #Function to get the % where experience_required is True for each occupation
        def compute_proportion_experience_required(occupation):
            total_entries = len(self.data[self.data['occupation'] == occupation])
            if total_entries == 0:
                return 0.0
            experience_required_entries = len(self.data[(self.data['occupation'] == occupation) & (self.data['experience_required'])])
            proportion_experience_required = experience_required_entries / total_entries
            return proportion_experience_required
        def count_str(data, column_name, search_string):
            pattern = fr"(?i)(?<!\S){re.escape(search_string)}(?!\S)"
            filtered_data = data[data[column_name].notna() & data[column_name].str.contains(pattern, regex=True)]
            count = filtered_data[column_name].str.contains(pattern, regex=True).sum()
            return count
        #Check how well each occupation matches with the programming types
        def compute_word_counts(data, occupation, word_list):
            occupation_data = data[data['occupation'] == occupation]
            count = 0
            for word in word_list:
                count += count_str(occupation_data, 'annonstext', word)
            return count
        #Word lists for matching
        web_development_words = ['html','css','javascript','front-end','frontend','user interface','ui','user experience','ux','användarupplevelse','design','web','website',
            'hemsida','web application','web applications','seo','e-commerce','wordpress','google','Facebook']
        general_purpose_programming_words = ['java', 'python', 'c++', 'ruby', 'Software development', 'mjukvaruutveckling', 'problem solving', 'problemlösning', 'Version control', 'ui', 'ux', 'ai', 'programming', 'coding', 'software', 'development']
        databases_data_manipulation_words = ['sql', 'database', 'query', 'data', 'update', 'uppdatera','databas', 'Data analysis', 'datanalys', 'ETL' ]
        scientific_mathematical_computing_words = ['math', 'statistics', 'simulation', 'AI', 'Artificial intelligence', 'Machine Learning', 'Algorithm', 'Algoritm', 'statistik', 'Analysis', 'Analys', 'Function', 'Funktion', 'Matematik', 'matte', 'Experiment', 'Data', 'Algebra', 'Research', 'Matrix', 'Probability', 'sannolikhet', 'theory', 'teori']
        not_interested_programming_words = ['programming', 'coding', 'software', 'development', 'java', 'python', 'c++', 'ruby', 'Software development', 'mjukvaruutveckling', 'problem solving', 'problemlösning', 'Version control', 'ui', 'ux', 'ai']

        #Creates an entry for each occupation and calls the appropriate functions for them
        occupation_profiles = {}
        for occupation in self.data['occupation']:
            if occupation not in occupation_profiles:
                occupation_entries = len(self.data[self.data['occupation'] == occupation])
                profile = {
                    'occupation_group': self.data.loc[self.data['occupation'] == occupation, 'occupation_group_name'].values[0],
                    'proportion_experience_required': compute_proportion_experience_required(occupation),
                    'Web Development': compute_word_counts(self.data, occupation, web_development_words) / occupation_entries,
                    'General-Purpose Programming': compute_word_counts(self.data, occupation, general_purpose_programming_words) / occupation_entries,
                    'Databases and Data Manipulation': compute_word_counts(self.data, occupation, databases_data_manipulation_words) / occupation_entries,
                    'Scientific and Mathematical Computing': compute_word_counts(self.data, occupation, scientific_mathematical_computing_words) / occupation_entries,
                    'Not interested in programming': compute_word_counts(self.data, occupation, not_interested_programming_words) / occupation_entries,
                    'Specific Languages': compute_word_counts(self.data, occupation, self.specific_languages)/occupation_entries
                }
                
                occupation_profiles[occupation] = profile

        return occupation_profiles

    def measure_similarity(self, user_preferences, occupation_profiles):
        similarity_scores = {}

        # Compare user preferences with occupation profiles and adjust the results by the weights
        for occupation, profile in occupation_profiles.items():
            if profile['occupation_group'] in self.selected_occupation_groups:
                profile['occupation_group'] = 1.0
            else: profile['occupation_group'] = 0.2
            if profile['proportion_experience_required'] <= user_preferences['total_experience']:
                profile['proportion_experience_required'] = 1.0
            else:
                profile['proportion_experience_required'] = (user_preferences['total_experience'] * profile['proportion_experience_required'])
            experience_similarity_weight = self.similarity_weights["experience_similarity"]
            experience_similarity = profile['proportion_experience_required'] * experience_similarity_weight
            # Calculate programming type similarity
            programming_type_similarity = 0.0
            for programming_type in self.programming_type:
                if programming_type in user_preferences and programming_type in profile:
                    programming_type_similarity = max(programming_type_similarity, profile[programming_type])
            type_similarity_weight = self.similarity_weights["type_similarity"]
            type_similarity = programming_type_similarity * type_similarity_weight
            language_similarity_weight = self.similarity_weights["language_similarity"]
            language_similarity = profile['Specific Languages'] * language_similarity_weight
            profile_similarity = (experience_similarity + type_similarity + language_similarity) * profile['occupation_group']
            similarity_scores[occupation] = profile_similarity

        return similarity_scores

    def rank_occupations(self, similarity_scores):
        ranked_occupations = []  # Create an empty list to store ranked occupations
        
        # Sort the occupations based on the similarity scores in descending order
        sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Append the occupations to the ranked_occupations list in the sorted order
        for occupation, scores in sorted_scores:
            ranked_occupations.append(occupation)
        
        return ranked_occupations
    def get_top_n_recommendations(self, ranked_occupations, similarity_scores, n):
        top_n_recommendations = []  # Create an empty list to store the top N recommendations
        
        # Select the top N occupations from the ranked_occupations list
        top_n_occupations = ranked_occupations[:n]
        
        # Retrieve the similarity scores for the top N occupations
        for occupation in top_n_occupations:
            rating = similarity_scores[occupation]
            top_n_recommendations.append((occupation, rating))
        
        return top_n_recommendations
