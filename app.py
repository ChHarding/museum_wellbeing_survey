# (base) amendatate@macbook-pro-164 museum_wellbeing_survey % python app.py
from flask import Flask, request, redirect, url_for, render_template
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csvfile' not in request.files:
        return redirect(request.url)
    file = request.files['csvfile']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.csv'):
        static_folder = os.path.join(app.root_path, 'static')
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
        filename = 'data.csv'
        file.save(os.path.join(static_folder, filename))
        return redirect(url_for('index'))
    return redirect(request.url)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)