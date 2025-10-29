# Pregnancy-Risk

This repository contains a small Flask application and a training script to predict pregnancy-related risk (High / Low) using a logistic regression model.

## What this repo contains

- `app.py` - Flask web application that serves a simple form (`/`) and a `/predict` POST endpoint which returns a risk label and probability.
- `model/train_model.py` - Script to train a logistic regression model using `data.csv` and save the trained model and scaler.
- `model/data.csv` - Dataset used for training (tabular features + `Risk Level` target).
- `model/model.pkl` and `model/scaler.pkl` - Trained artifacts expected by `app.py` (may be created by the training script).
- `templates/` - HTML templates used by the Flask app (`index.html`, `result.html`).

## Quick overview of how it works

- The training script (`model/train_model.py`) loads `data.csv`, preprocesses (median imputation and standard scaling), trains a `LogisticRegression`, and writes the model and scaler as pickles.
- The Flask app (`app.py`) loads the saved `model/model.pkl` and `model/scaler.pkl` at startup. When a user submits the form, the app reads numeric fields in a specific order, converts them to floats, scales them with the loaded scaler, and uses the model to return a risk label and probability.

## Required Python packages

- Python 3.8+ (recommended)
- Flask
- scikit-learn
- pandas
- numpy

You can install these with pip. From PowerShell (Windows):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install flask scikit-learn pandas numpy
```

If you prefer, create a `requirements.txt` with these packages and run `pip install -r requirements.txt`.

## Training the model

1. Put your dataset in `model/data.csv`. The script expects these columns (exact names used in `train_model.py`):

	 - `Age`
	 - `Systolic BP`
	 - `Diastolic`
	 - `BS`
	 - `Body Temp`
	 - `BMI`
	 - `Previous Complications`
	 - `Preexisting Diabetes`
	 - `Gestational Diabetes`
	 - `Mental Health`
	 - `Heart Rate`
	 - `Risk Level` (target column: values `Low` or `High`)

2. Run the training script from the repository root:

```powershell
python model\train_model.py
```

Notes about output paths:
- `model/train_model.py` saves `model.pkl` and `scaler.pkl` using relative filenames. If you run the script from the repository root (the usual case), this will create `model\model.pkl` and `model\scaler.pkl` because the script is located in the `model` folder. After training, confirm that `model\model.pkl` and `model\scaler.pkl` exist — these are required by `app.py`.

Important: the script currently prints `Model, scaler, and imputer saved successfully!`, but it does not actually save the imputer object. If you expect to handle missing inputs the same way at inference, either save the imputer in the training script or ensure your app handles missing fields consistently.

## Running the Flask app (development)

From the repository root (PowerShell on Windows):

```powershell
venv\Scripts\Activate.ps1   # if you created/activated the venv earlier
python app.py
```

Open a browser to http://127.0.0.1:5000/ to view the form.

## Form field names and ordering (very important)

`app.py` expects numeric inputs in this exact order when forming the feature vector for the scaler/model:

1. `age`               -> corresponds to `Age`
2. `sysbp`             -> corresponds to `Systolic BP`
3. `diabp`             -> corresponds to `Diastolic`
4. `bs`                -> corresponds to `BS`
5. `bt`                -> corresponds to `Body Temp`
6. `bmi`               -> corresponds to `BMI`
7. `pc`                -> corresponds to `Previous Complications`
8. `preexidia`         -> corresponds to `Preexisting Diabetes`
9. `gesdia`            -> corresponds to `Gestational Diabetes`
10. `mh`               -> corresponds to `Mental Health`
11. `hr`               -> corresponds to `Heart Rate`

`app.py` also reads optional `name` and `email` fields from the form for friendly output.

When building or editing the HTML form (`templates/index.html`), make sure your input `name` attributes match the field names above.

## Example prediction flow

- User fills the form and submits (POST `/predict`).
- The server reads and coerces values to floats (invalid or missing values default to `0.0`).
- The server scales the numeric vector with the loaded `scaler` and calls `model.predict_proba(...)` and `model.predict(...)`.
- The returned page shows `High Risk` or `Low Risk` and the probability percentage.

## Troubleshooting

- FileNotFoundError for model files: confirm `model\model.pkl` and `model\scaler.pkl` exist. If they were created somewhere else, copy them into the `model` folder or update the paths in `app.py`.
- Missing input values: `app.py` currently replaces invalid or missing numeric inputs with `0.0`. This can bias predictions. Better approaches:
	- Save the imputer used at training time and load it at inference, applying the same imputation.
	- Validate user input on the client side and server side, and refuse/ask for missing required fields.
- Version mismatches: if you get pickle load errors, ensure scikit-learn versions used for training and inference are compatible.
  ## gunicorn
- for render deployment
## Next steps / Improvements

- Save the imputer object when training and load it in `app.py` to guarantee consistent imputation.
- Add a `requirements.txt` and/or `pyproject.toml` to pin package versions.
- Add simple unit tests for the predict endpoint and training script.
- Consider exposing a small API (JSON) for programmatic use instead of just HTML forms.

## License

This project does not include a license file; add one if you want to open-source the code.

---

If you'd like, I can also:

- add a `requirements.txt` with pinned versions,
- save and load the imputer in `train_model.py` and update `app.py` accordingly, or
- add a minimal test script that calls `/predict` with example data and asserts expected response structure.

Tell me which of those you'd like me to do next.
