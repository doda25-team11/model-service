"""
Flask API of the SMS Spam detection model model.
"""
import joblib
from flask import Flask, jsonify, request
from flasgger import Swagger
import pandas as pd
import os

from text_preprocessing import prepare, _extract_message_len, _text_process

app = Flask(__name__)
swagger = Swagger(app)

# We load the model before so that we don't have to do it every time we do a predict()
MODEL_DIR = os.getenv("MODEL_DIR", "/app/model")

# Check if the path exists, it should using the container but when running normally it doesn't so fall back to original
if not os.path.exists(MODEL_DIR):
    MODEL_DIR = "output"

MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

model = joblib.load(MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict whether an SMS is Spam.
    ---
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: message to be classified.
          required: True
          schema:
            type: object
            required: sms
            properties:
                sms:
                    type: string
                    example: This is an example of an SMS.
    responses:
      200:
        description: "The result of the classification: 'spam' or 'ham'."
    """
    input_data = request.get_json()
    sms = input_data.get('sms')
    processed_sms = prepare(sms)
    #model = joblib.load('output/model.joblib')
    prediction = model.predict(processed_sms)[0]
    
    res = {
        "result": prediction,
        "classifier": "decision tree",
        "sms": sms
    }
    print(res)
    return jsonify(res)

if __name__ == '__main__':
    #clf = joblib.load('output/model.joblib')
    app.run(host="0.0.0.0", port=8081, debug=True)
