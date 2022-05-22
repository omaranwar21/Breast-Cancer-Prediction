# from crypt import methods
import numpy as np
import pickle
from flask import Flask, url_for, render_template, request
model = pickle.load(open("model.pkl", "rb"))

app = Flask(__name__, template_folder="templates")

@app.route('/')
def website():
    return render_template('WellBeing.html')

@app.route('/', methods=['POST'])
def predict():
    print(request.form.values())
    formValues = [j for j in request.form.values()]
    name = formValues[0]
    formValues.pop(0)
    floatFeatures = [float(j) for j in formValues]
    print(name)
    features = [np.array (floatFeatures)]
    prediction = model.predict (features)
    if prediction == 1:
        return render_template('WellBeing.html', state= "Unfortunatly", predictionText=", It is a Tumor.")
    else:
        return render_template('WellBeing.html', state= "Congratulations!", predictionText= "It is a Benign Tumor.")
       
# @wellBeing.route('/', methods['post'])
# def result():

#     return render_template('WellBeing.html')

if __name__ == "__main__":
    app.run(debug=True)

