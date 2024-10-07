from flask import Flask, render_template

app = Flask(__name__)

# Home page (Index)
@app.route('/')
def index():
    return render_template('index.html')

# About Me page
@app.route('/about')
def about():
    return render_template('about.html')

# Projects page
@app.route('/projects')
def projects():
    return render_template('projects.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
