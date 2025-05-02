import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv(r"C:\Users\user\Desktop\rdr\rdr\data_file.csv")  # Ensure this file exists

# Remove unnecessary columns
df_cleaned = df.drop(columns=["FileName", "md5Hash"])
# Split into features (X) and target (y)
X = df_cleaned.drop(columns=["Benign"])
y = df_cleaned["Benign"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Save model & scaler
joblib.dump(model, "ransomware_detection_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("Model training complete! Model and scaler saved.")
