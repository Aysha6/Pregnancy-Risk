# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
import pickle

# ✅ Load dataset
df = pd.read_csv('data.csv')

# ✅ Define feature and target columns
feature_cols = [
    'Age', 'Systolic BP', 'Diastolic', 'BS', 'Body Temp', 'BMI',
    'Previous Complications', 'Preexisting Diabetes', 'Gestational Diabetes',
    'Mental Health', 'Heart Rate'
]
target_col = 'Risk Level'

# ✅ Drop rows where target is missing
df = df.dropna(subset=[target_col])

# ✅ Convert Risk Level → numeric (Low=0, High=1)
df[target_col] = df[target_col].map({'Low': 0, 'High': 1})

# ✅ Handle any still-missing target values (after mapping)
df = df.dropna(subset=[target_col])

# ✅ Extract features (X) and target (y)
X = df[feature_cols]
y = df[target_col].astype(int)

# ✅ Impute missing numeric data
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

# ✅ Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42
)

# ✅ Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ✅ Train logistic regression model
model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

# ✅ Save model components
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Model, scaler, and imputer saved successfully!")
print("Training Accuracy:", round(model.score(X_train_scaled, y_train), 3))
print("Testing Accuracy:", round(model.score(X_test_scaled, y_test), 3))
