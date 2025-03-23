from flask import Flask, request, jsonify

app = Flask(__name__)

# Carbon emission factors (in kg CO2 per km)
emission_factors = {
    'car': 0.21,
    'bus': 0.11,
    'train': 0.05,
    'flight': 0.15,
    'bike': 0.0
}

@app.route('/')
def home():
    return jsonify({"student_number": 200582781})

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req.get('queryResult', {}).get('intent', {}).get('displayName')

    if intent == 'CalculateCarbonFootprint':
        parameters = req['queryResult']['parameters']
        transport = parameters.get('transport_type', '').lower()
        distance = parameters.get('distance', 0)

        factor = emission_factors.get(transport, 0.2)  # fallback factor
        footprint = round(factor * distance, 2)

        response_text = (
            f"Your estimated carbon footprint for traveling {distance} km by {transport} "
            f"is {footprint} kg of CO2."
        )
    else:
        response_text = "I'm not sure how to help with that."

    return jsonify({"fulfillmentText": response_text})

if __name__ == '__main__':
    app.run(debug=True)
