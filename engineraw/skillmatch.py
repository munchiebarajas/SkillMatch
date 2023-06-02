import json
from flask import Flask, render_template, request, jsonify
import pandas as pd
from recommendation_engineraw import RecommendationEngine


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionpage')
def questions_page():
    return render_template('questionpage.html')

@app.route('/questionpage2', methods=['POST'])
def question_page2():
    # Get the selected occupation_group_name checkboxes
    occupation_group_names = request.form.getlist('occupation_group_name[]')
    # Load existing data from the JSON file
    with open('user_preference.json', 'r') as file:
        data = json.load(file)
    # Add the new data to the existing dictionary
    data['occupation_group_name'] = occupation_group_names
    # Write the updated data to the JSON file
    with open('user_preference.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    return render_template('questionpage2.html')

@app.route('/questionpage3', methods=['POST'])
def question_page3():
    # Get the values from the sliders
    experience = request.form.getlist('Experience[]')
    experience = [int(exp) for exp in experience]
    # Load existing data from the JSON file
    with open('user_preference.json', 'r') as file:
        data = json.load(file)
    # Add the new data to the existing dictionary
    data['Experience'] = experience
    # Write the updated data to the JSON file
    with open('user_preference.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    return render_template('questionpage3.html')

@app.route('/result', methods=['POST'])
def result():
    # Get the email address from the form
    programming_types = request.form.getlist('programming_type[]')
    specific_languages = request.form.getlist('specific_languages[]')
    # Load existing data from the JSON file
    with open('user_preference.json', 'r') as file:
        data = json.load(file)
    # Add the new data to the existing dictionary
    data['programming_type'] = programming_types
    data['specific_languages'] = specific_languages
    # Write the updated data to the JSON file
    with open('user_preference.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

    dataset = pd.read_csv('jobtech_2023clean.csv')
    profiles = pd.read_csv('occupation_profiles.csv')
    engine = RecommendationEngine(dataset, profiles, data)
    recommendation = engine.create_recommendation()
    results = recommendation.run()
    job_descriptions = get_job_description(results)

    return render_template('result.html', results=results, job_descriptions=job_descriptions)

def get_job_description(results):
    descriptions = {}
    with open('occupation_descriptions.json', 'r', encoding='utf-8') as file:
        descriptions = json.load(file)

    job_descriptions = {}
    for job, _ in results:
        if job in descriptions:
            job_descriptions[job] = descriptions[job]

    return job_descriptions

if __name__ == '__main__':
    app.run()
