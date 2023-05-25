from flask import Flask, render_template, request, url_for, redirect
from recommendation_engine import RecommendationEngine, Recommendation

app = Flask(__name__)

recommendation_engine = RecommendationEngine()
recommendation_engine.load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions.html', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        selected_occupation_groups = request.form.getlist('occupation_group')
        return redirect(url_for('recommendation', occupation_groups=selected_occupation_groups))
    return render_template('questions.html')

@app.route('/questions2.html', methods=['GET', 'POST'])
def questions2():
    if request.method == 'POST':
        # Handle the form submission or any logic specific to questions2.html
        # You can access form data using request.form.getlist() or request.form['field_name']
        return redirect(url_for('recommendation'))  # Redirect to the next page after form submission
    return render_template('questions2.html')

@app.route('/recommendation', methods=['GET'])
def recommendation():
    occupation_groups = request.args.getlist('occupation_groups')
    # Pass the occupation groups to the recommendation engine
    recommendation = recommendation_engine.create_recommendation(occupation_groups)
    # Render the recommendation template and pass the recommendation data
    return render_template('recommendation.html', recommendation=recommendation)

if __name__ == '__main__':
    app.run()