# app.py
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# ✅ Load the trained model and scaler
with open('model/model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('model/scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    form_data = request.form.to_dict()

    # Extract name and email (optional)
    name = form_data.get('name', '')
    email = form_data.get('email', '')

    # ✅ Define numeric fields in correct order
    numeric_fields = [
        'age', 'sysbp', 'diabp', 'bs', 'bt', 'bmi',
        'pc', 'preexidia', 'gesdia', 'mh', 'hr'
    ]

    # ✅ Convert to numeric safely
    numeric_values = []
    for field in numeric_fields:
        value = form_data.get(field)
        try:
            numeric_values.append(float(value))
        except (TypeError, ValueError):
            numeric_values.append(0.0)

    # ✅ Scale and predict
    scaled_values = scaler.transform([numeric_values])
    prob = model.predict_proba(scaled_values)[0][1]  # probability of class 1
    prediction = int(model.predict(scaled_values)[0])

    # ✅ Interpret results
    result = "High Risk" if prediction == 1 else "Low Risk"
    probability_percent = round(prob * 100, 2)

    return render_template(
        'result.html',
        name=name,
        prediction=result,
        probability=probability_percent
    )

if __name__ == '__main__':
    app.run(debug=True)
