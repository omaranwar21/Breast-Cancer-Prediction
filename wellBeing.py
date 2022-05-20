import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template

wellBeing = Flask(__name__, template_folder="templetes")

if __name__ == '__main__':
    wellBeing.run(debug=True) 

@wellBeing.route('WellBeing.html?#result', methods=['GET', 'POST'])
def wellBeing():
    if request.method == 'POST':
        # Get the file from post request
        text = request.form['text']
        
        wellBeing = wellBeing()
        
        return wellBeing.predict(text)
    return None