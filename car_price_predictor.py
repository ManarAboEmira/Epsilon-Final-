import sys
import joblib
import pandas as pd
from flask import Flask, request, render_template_string

sys.path.append("_")

app = Flask(__name__)
model = joblib.load("E:/epsilon/ff/model.pkl")

df = pd.read_csv("E:/epsilon/ff/Cardetails.csv")
brands = df['name'].unique()

conversion_rate = 0.012  # 1 INR = 0.012 USD

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error_message = None
    if request.method == "POST":
        try:
            # Get form data and ensure correct types
            year = int(request.form["year"])
            mileage = float(request.form["mileage"].split()[0].replace(',', ''))
            max_power = float(request.form["max_power"].split()[0].replace(',', ''))
            engine = float(request.form["engine"].split()[0].replace(',', ''))
            brand = request.form["brand"]
            transmission = int(request.form["transmission"])
            seller_type = int(request.form["seller_type"])
            fuel = int(request.form["fuel"])
            owner = int(request.form["owner"])
            km_driven = float(request.form["km_driven"].split()[0].replace(',', ''))
            seats = int(request.form["seats"])

            # Convert categorical brand to numeric
            brand_index = list(brands).index(brand) + 1

            # Ensure the model input array includes all features
            input_data = [[year, mileage, max_power, engine, brand_index, transmission, seller_type, fuel, owner, km_driven, seats]]

            # Predict the price
            price_inr = model.predict(input_data)[0]
            # Convert price from INR to USD
            prediction = price_inr * conversion_rate

        except ValueError as e:
            error_message = f"Input error: {e}"
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Car Price Prediction</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #CBCE91FF;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                width: 100%;
            }

            h1 {
                text-align: center;
                color: #CBCE91FF;
            }

            form {
                display: flex;
                flex-direction: column;
            }

            label {
                margin-bottom: 10px;
                color: #EA738DFF;
                font-size: 20px;  # Increase the label font size
            }

            input[type="text"],
            input[type="number"],
            select {
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
            }

            button {
                background-color: #CBCE91FF;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background-color: #EA738DFF;
            }

            .result {
                text-align: center;
                font-size: 24px;
                margin-top: 20px;
                color: #333;
            }

            .error {
                text-align: center;
                color: red;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Car Price Prediction</h1>
            <form method="POST">
                <label for="year">Year</label>
                <input type="number" id="year" name="year" required>

                <label for="mileage">Mileage (km/l)</label>
                <input type="text" id="mileage" name="mileage" required>

                <label for="max_power">Max Power (bhp)</label>
                <input type="text" id="max_power" name="max_power" required>

                <label for="engine">Engine (cc)</label>
                <input type="text" id="engine" name="engine" required>

                <label for="brand">Brand</label>
                <select id="brand" name="brand" required>
                    {% for brand in brands %}
                        <option value="{{ brand }}">{{ brand }}</option>
                    {% endfor %}
                </select>

                <label for="transmission">Transmission</label>
                <select id="transmission" name="transmission" required>
                    <option value="1">Manual</option>
                    <option value="2">Automatic</option>
                </select>

                <label for="seller_type">Seller Type</label>
                <select id="seller_type" name="seller_type" required>
                    <option value="1">Individual</option>
                    <option value="2">Dealer</option>
                    <option value="3">Trustmark Dealer</option>
                </select>

                <label for="fuel">Fuel Type</label>
                <select id="fuel" name="fuel" required>
                    <option value="1">Diesel</option>
                    <option value="2">Petrol</option>
                    <option value="3">LPG</option>
                    <option value="4">CNG</option>
                </select>

                <label for="owner">Owner Type</label>
                <select id="owner" name="owner" required>
                    <option value="1">First Owner</option>
                    <option value="2">Second Owner</option>
                    <option value="3">Third Owner</option>
                    <option value="4">Fourth & Above Owner</option>
                    <option value="5">Test Drive Car</option>
                </select>

                <label for="km_driven">Kilometers Driven</label>
                <input type="text" id="km_driven" name="km_driven" required>

                <label for="seats">Seats</label>
                <input type="number" id="seats" name="seats" required>

                <button type="submit">Predict</button>
            </form>

            {% if prediction %}
            <div class="result">
                Predicted Price: ${{ prediction|round(2) }}
            </div>
            {% endif %}

            {% if error_message %}
            <div class="error">
                {{ error_message }}
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    ''', prediction=prediction, error_message=error_message, brands=brands)

if __name__ == "__main__":
    app.run(debug=True)
