from flask import Flask, render_template, request, url_for, redirect, session
from recommendation_engine import RecommendationEngine, Recommendation

app = Flask(__name__)
app.secret_key = 'skillmatch'

recommendation_engine = RecommendationEngine()
recommendation_engine.load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions.html', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        selected_occupation_groups = request.form.getlist('occupation_group')
        # session['selected_occupation_groups'] = selected_occupation_groups
        print("Occupation Groups:", selected_occupation_groups)
        return redirect(url_for('questions2'))  # Redirect to questions2.html
    return render_template('questions.html')


@app.route('/questions2.html', methods=['GET', 'POST'])
def questions2():
    if request.method == 'POST':
        experience = [int(request.form['slider1']), int(request.form['slider2'])]
        session['experience'] = experience
        print("Experience:", experience)
        return redirect(url_for('index'))  # Redirect to index.html
    return render_template('questions2.html')

"""@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    occupation_groups = session.get('answers_question_1', [])  # Retrieve saved answers for question 1
    # Pass the occupation groups to the recommendation engine
    recommendation = recommendation_engine.create_recommendation(occupation_groups)
    # Render the recommendation template and pass the recommendation data
    return render_template('recommendation.html', recommendation=recommendation)
"""
if __name__ == '__main__':
    app.run()