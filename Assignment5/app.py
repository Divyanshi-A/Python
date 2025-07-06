import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template_string, request

# Load trained Ridge model
with open('ridge_model.pkl', 'rb') as f:
    model=pickle.load(f)

# Features the model expects and what they mean
FEATURES=[
    ('OverallQual', 'Overall Quality (1–10, higher is better)'),
    ('GrLivArea', 'Above-ground Living Area (sq ft, e.g., 1200–2500)'),
    ('GarageCars', 'Garage Capacity (number of cars, 0–4)'),
    ('TotalSF', 'Total Floor Area (sq ft, e.g., 1000–4000)'),
    ('HouseAge', 'Age of House (years, e.g., 0–100)')
]

# Flask app
app=Flask(__name__)

# HTML UI Template
HTML="""
<!DOCTYPE html>
<html>
<head>
    <title>House Price Predictor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #1e1e2f;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        .container {
            background-color: #2c2c3c;
            border-radius: 15px;
            padding: 30px;
            margin-top: 50px;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
        }
        .form-control {
            background-color: #333344;
            border: none;
            border-radius: 12px;
            color: #ffffff;
        }
        .form-control::placeholder {
            color: #cccccc;
        }
        .btn-primary {
            background-color: #5a78ff;
            border: none;
            border-radius: 12px;
            font-weight: 500;
        }
        .alert-success {
            background-color: #3d7c3d !important;
            border: none;
            border-radius: 10px;
            color: #ffffff;
        }
        label {
            margin-top: 10px;
            font-size: 0.95rem;
        }
        small {
            color: #bbbbbb;
        }
    </style>
</head>
<body>
<div class="container">
    <h2 class="mb-4">🏡 House Price Prediction</h2>
    <form method="post">
        <div class="row g-3">
            {% for feature, hint in features %}
                <div class="col-md-6">
                    <label>{{ feature }}</label>
                    <input name="{{ feature }}" class="form-control" placeholder="Enter {{ feature }}" required>
                    <small>{{ hint }}</small>
                </div>
            {% endfor %}
        </div>
        <button class="btn btn-primary mt-4 px-4 py-2" type="submit">Predict Price</button>
    </form>

    {% if price is not none %}
        <div class="alert alert-success mt-4">
            Predicted Sale Price: <strong>${{ price }}</strong>
        </div>
    {% endif %}
</div>
</body>
</html>
"""

# Flask route
@app.route('/', methods=['GET', 'POST'])
def predict():
    price=None
    if request.method=='POST':
        try:
            # Build DataFrame with column names for model
            values_dict={feat: [float(request.form.get(feat, 0))] for feat, _ in FEATURES}
            df_input=pd.DataFrame(values_dict)
            log_price=model.predict(df_input)[0]
            price=round(np.expm1(log_price), 2)
        except Exception as e:
            print("Prediction error:", e)
            price="Invalid input."
    return render_template_string(HTML, price=price, features=FEATURES)

# Run server
if __name__=='__main__':
    app.run(debug=True)
