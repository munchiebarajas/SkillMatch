from flask import Flask
app = Flask(__name__)

@app.route('/static/css/style.css')
def serve_css():
    return app.send_static_file('css/style.css')    

<link rel="stylesheet" type="text/css" href="{{ url_for('serve_css') }}">

if __name__ == '__main__':
    app.run(debug=True)