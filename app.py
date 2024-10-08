from flask import Flask, render_template
from artstractaguiar.app import artstractaguiar_app  # Import the second app

app = Flask(__name__)

# Home page (Index)
@app.route('/')
def index():
    return render_template('index.html')

# About Me page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')  # Projects page, including Artstractaguiar

@app.route('/services')
def services():
    return render_template('services.html')  # Services page

app.register_blueprint(artstractaguiar_app, url_prefix='/artstractaguiar')

if __name__ == '__main__':
    app.run(debug=True)
