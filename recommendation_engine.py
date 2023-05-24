import json
from questions import get_selected_occupation_groups, ask_experience, ask_programming_type, ask_specific_languages

class RecommendationEngine:
    def __init__(self, data):
        self.data = data

    def create_recommendation(self):
        # Define question and answer weights

        question_weights = {
            "occupation_groups": 1.0,
            "experience": 1.0,
            "programming_type": 1.0,
            "specific_languages": 1.0
        }

        answer_weights = {
            "occupation_groups": {
                "selected_occupations": 1.0
            },
            "experience": {
                "has_experience": 1.0
            },
            "programming_type": {
                "selected_types": 1.0
            },
            "specific_languages": {
                "selected_languages": 1.0
            }
        }

        # Preset user inputs (for testing and development)
        selected_occupation_groups = ['Mjukvaru- och systemutvecklare m.fl.']
        experience = True
        programming_type = ['General-Purpose Programming', 'Web Development']
        specific_languages = ['Python', 'CSS', 'C#']

        """
        # Gather user input
        selected_occupation_groups = get_selected_occupation_groups()
        experience = ask_experience()
        programming_type = ask_programming_type()
        specific_languages = ask_specific_languages(programming_type)
        """
        # Create recommendation object
        recommendation = Recommendation(
            self.data,
            selected_occupation_groups,
            experience,
            programming_type,
            specific_languages,
            question_weights,
            answer_weights
        )

        return recommendation

class Recommendation:
    def __init__(self, data, selected_occupation_groups, experience, programming_type, specific_languages,
                 question_weights, answer_weights):
        self.data = data
        self.selected_occupation_groups = selected_occupation_groups
        self.experience = experience
        self.programming_type = programming_type
        self.specific_languages = specific_languages
        self.question_weights = question_weights
        self.answer_weights = answer_weights

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
        recommended_occupations = self.get_top_n_recommendations(ranked_occupations, n=10)
        return recommended_occupations

    def calculate_user_preferences(self):
        # Implement the calculation of user preferences based on question/answer weights and user input
        # Calculate occupation group preferences based on selected occupation groups
        occupation_group_preferences = {group: 1.0 if group in self.selected_occupation_groups else 0.0
                                        for group in self.data['occupation_group_name']}
        return occupation_group_preferences

    def compute_occupation_profiles(self):
        # Implement the computation of occupation profiles from the data
        pass

    def measure_similarity(self, user_preferences, occupation_profiles):
        # Implement the calculation of similarity scores between user preferences and occupation profiles
        pass

    def rank_occupations(self, similarity_scores):
        # Implement the ranking of occupations based on similarity scores
        pass

    def get_top_n_recommendations(self, ranked_occupations, n):
        # Implement the selection of top N occupations as recommendations
        pass
