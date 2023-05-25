from flask import Flask, render_template
from recommendation_engine import RecommendationEngine, Recommendation

app = Flask(__name__)

recommendation_engine = RecommendationEngine()
recommendation_engine.load_data()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/questions.html')
def questions():
    return render_template('questions.html')

if __name__ == '__main__':
    app.run()