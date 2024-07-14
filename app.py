# open new terminal
# (base) amendatate@macbook-pro-164 HCI584 % cd museum_wellbeing_survey
# (base) amendatate@macbook-pro-164 museum_wellbeing_survey % python app.py
# open http://127.0.0.1:8001/

from flask import Flask, render_template

app = Flask(__name__)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True, port=8001)