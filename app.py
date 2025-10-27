from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# ✅ Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # ✅ Get form data
    form_data = request.form.to_dict()

    # ✅ Extract non-numeric info
    name = form_data.get('name')
    email = form_data.get('email')

    # ✅ Define numeric input field names (must match your HTML form names)
    numeric_fields = [
        'age', 'sysbp', 'diabp', 'bs', 'bt', 'bmi',
        'pc', 'preexidia', 'gesdia', 'mh', 'hr'
    ]

    # ✅ Safely convert numeric inputs to float
    numeric_values = []
    for field in numeric_fields:
        value = form_data.get(field)
        if value is None or value == "":
            numeric_values.append(0.0)  # default if empty
        else:
            numeric_values.append(float(value))

    # ✅ Make prediction
    prediction = model.predict([numeric_values])[0]

    # ✅ Interpret result
    result = "High Risk" if prediction == 1 else "Low Risk"

    # ✅ Return result page
    return render_template('result.html', name=name, prediction=result)


if __name__ == '__main__':
    app.run(debug=True)



