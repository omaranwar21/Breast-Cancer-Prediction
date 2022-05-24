import numpy as np
import pickle
from flask import Flask, url_for, render_template, request
model = pickle.load(open("model.pkl", "rb"))

wellBeing = Flask(__name__, template_folder="templates")

@wellBeing.route('/')
def website():
    return render_template('WellBeing.html')

@wellBeing.route('/test')
def test():
    return render_template('result.html')

@wellBeing.route('/result', methods=['POST'])
def result():
    request.form.values()
    formValues = [j for j in request.form.values()]
    name = formValues[0]
    print(name)
    formValues.pop(0)
    floatFeatures = [float(j) for j in formValues]
    features = [np.array (floatFeatures)]
    prediction = int(model.predict (features))
    print(features)
    print(prediction)

    if prediction == 1:
        prediction_text = 'Malignant'
    elif prediction == 0:
        prediction_text = 'Benign'

    return render_template ('result.html', prediction_text = 'The Tumor is {}'.format(prediction_text),)
       
if __name__ == "__main__":
    wellBeing.run(debug=True) 

