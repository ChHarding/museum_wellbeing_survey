# open new terminal
# (base) amendatate@macbook-pro-164 HCI584 % cd museum_wellbeing_survey
# (base) amendatate@macbook-pro-164 museum_wellbeing_survey % flask run

import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Get list of all files in the static directory
    static_files = os.listdir(app.static_folder)
    
    # Filter to only include image files (you can adjust this as needed)
    image_filenames = [filename for filename in static_files if filename.endswith(('jpg', 'jpeg', 'png', 'gif'))]
    
    # Render the template and pass the image filenames to it
    return render_template('index.html', image_filenames=image_filenames)

if __name__ == '__main__':
    app.run(debug=True)