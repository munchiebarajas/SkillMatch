import json
import re
import pandas as pd
import numpy as np
#from questionsraw import get_selected_occupation_groups, ask_experience, ask_programming_type, ask_specific_languages

class RecommendationEngine:
    def __init__(self, data, profiles):
        self.data = data
        self.profiles = profiles
        #self.preferences = preferences

    def create_recommendation(self):
        # Load question and answer weights from the JSON file
        with open('weight_settingsraw.json') as file:
            weight_settings = json.load(file)

        question_weights = weight_settings['question_weights']
        answer_weights = weight_settings['answer_weights']
        similarity_weights = weight_settings['similarity_weights']

        
        selected_occupation_groups = ['Mjukvaru- och systemutvecklare m.fl.']
        experience = [2, 2]
        programming_type = ['Web Development', 'General-Purpose Programming']
        specific_languages = ['Python', 'HTML', 'CSS']
        '''
        selected_occupation_groups = get_selected_occupation_groups()
        experience = ask_experience()
        programming_type = ask_programming_type()
        specific_languages = ask_specific_languages(programming_type)
        '''

        # Create recommendation object
        recommendation = Recommendation(
            self.data,
            self.profiles,
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
    def __init__(self, data, profiles, selected_occupation_groups, experience, programming_type, specific_languages,
                 question_weights, answer_weights, similarity_weights):
        self.data = data
        self.occupation_profiles = profiles
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
        occupation_profiles = self.occupation_profiles

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

        work_experience = self.experience[0]
        education_experience = self.experience[1]

        experience_preferences = {
            "total_experience": (work_experience * work_experience_weight) + (education_experience * education_experience_weight)
        }

        # Add programming type preferences with weights
        programming_type_preferences = {
            programming_type: self.answer_weights.get("programming_type", {}).get("selected_types", 0.0)
            for programming_type in self.programming_type
        }

        # Add specific language preferences with weights
        specific_language_preferences = {
            language: self.answer_weights.get("specific_languages", {}).get("selected_languages", 0.0)
            for language in self.specific_languages
        }


        # Combine preferences into user_preferences dict
        user_preferences = {}
        user_preferences.update(occupation_group_preferences)
        user_preferences.update(experience_preferences)
        user_preferences.update(programming_type_preferences)
        user_preferences.update(specific_language_preferences)

        return user_preferences
    
    #Measure the similarity between preferences and occupation profiles
    def measure_similarity(self, user_preferences, occupation_profiles):
        similarity_scores = {}
        # Compare user preferences with occupation profiles and adjust the results by the weights
        for index, profile in occupation_profiles.iterrows():
            occupation = profile['Occupation']
            occupation_group_name = profile['occupation_group_name']
            
            # Compare occupation group pref
            if occupation_group_name in self.selected_occupation_groups:
                occupation_group_similarity = 1.0
            else:
                occupation_group_similarity = 0.4
                
            # Compare the experience
            if user_preferences['total_experience'] >= profile['Experience']:
                experience_similarity = 1.0
            else:
                profile_experience = profile['Experience']
                user_experience = user_preferences['total_experience']
                experience_similarity = min(user_experience / profile_experience, 1.0)
            
            # Calculate programming type similarity
            programming_type_similarity = 0.0
            for programming_type in self.programming_type:
                if programming_type in user_preferences and programming_type in profile:
                    programming_type_similarity = max(programming_type_similarity, profile[programming_type])
            type_similarity_weight = self.similarity_weights["type_similarity"]
            type_similarity = programming_type_similarity * type_similarity_weight
            
            # Calculate prog language similarity
            language_similarity_weight = self.similarity_weights["language_similarity"]
            language_similarity = sum(profile[language] for language in self.specific_languages) * language_similarity_weight
            
            # Combine the similarities to create a profile similarity score
            profile_similarity = (experience_similarity + type_similarity + language_similarity) * occupation_group_similarity
            similarity_scores[occupation] = profile_similarity

        return similarity_scores
    
    #Rank the similarity scores
    def rank_occupations(self, similarity_scores):
        ranked_occupations = []  # Create an empty list to store ranked occupations
        
        # Sort the occupations based on the similarity scores in descending order
        sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Append the occupations to the ranked_occupations list in the sorted order
        for occupation, scores in sorted_scores:
            ranked_occupations.append(occupation)
        
        return ranked_occupations
    
    #Get the top N recommendations and their rating
    def get_top_n_recommendations(self, ranked_occupations, similarity_scores, n):
        top_n_recommendations = []  # Create an empty list to store the top N recommendations
        
        # Select the top N occupations from the ranked_occupations list
        top_n_occupations = ranked_occupations[:n]
        
        # Retrieve the similarity scores for the top N occupations
        for occupation in top_n_occupations:
            rating = similarity_scores[occupation]
            top_n_recommendations.append((occupation, rating))
        
        return top_n_recommendations
