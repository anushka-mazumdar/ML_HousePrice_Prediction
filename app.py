import pandas as pd
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the data and model
df = pd.read_csv("cleaned_data.csv")
pipe = pickle.load(open("RidgeModel.pkl", "rb"))

@app.route('/')
def index():
    locations = sorted(df["location"].unique())
    return render_template("index.html", locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve form data
    locations = request.form.get("Location")
    bhk = request.form.get("bhk")
    balcony = request.form.get("balcony")
    sqft = request.form.get("total_sqft")

    # Check for missing data
    if not all([locations, bhk, balcony, sqft]):
        return "Please fill in all the required fields."

    # Convert total_sqft to float and handle errors
    try:
        sqft = float(sqft)
    except ValueError:
        return "Invalid input for total_sqft. Please enter a numeric value."

    # Create a DataFrame with the input values
    input_df = pd.DataFrame([[locations, sqft, bhk, balcony]], columns=['location', 'total_sqft', 'bhk', 'balcony'])

    # Make a prediction
    prediction = pipe.predict(input_df)[0] * 1e5

    return str(np.round(prediction, 2))

if __name__ == "__main__":
    app.run(debug=True, port=5500)
