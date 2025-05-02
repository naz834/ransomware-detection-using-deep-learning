import pandas as pd
import requests
import json

# Load test data
df = pd.read_csv(r"C:\Users\user\Desktop\rdr\rdr\data_file.csv")

# Flask API URL
API_URL = "http://127.0.0.1:5000/predict"

# Loop through each sample and send for prediction
for index, row in df.iterrows():
    data = row.to_dict()  # Convert row to dictionary format
    response = requests.post(API_URL, json=data)

    # Print the response
    print(f"Sample {index + 1}: {response.json()}")
