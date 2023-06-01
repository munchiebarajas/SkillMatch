import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionpage')
def questions_page():
    return render_template('questionpage.html')

@app.route('/save-data', methods=['POST'])
def save_data():
    name = request.form.get('name')
    email = request.form.get('email')

    # Create a dictionary of the form data
    data = {'Name': name, 'Email': email}

    # Define the JSON file path
    json_file = 'user_preference.json'  # Replace with your desired file path

    # Write the data to the JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file)

    return 'Data saved successfully!'

if __name__ == '__main__':
    app.run()
