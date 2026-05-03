import pickle
import json
import os
from flask import Flask, request

app = Flask(__name__)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        predictions = model.predict(data['instances'])
        return {'predictions': predictions.tolist()}
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)