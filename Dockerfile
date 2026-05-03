FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir scikit-learn flask

COPY model.pkl .

EXPOSE 8080

CMD ["python", "-c", """
import pickle
import json
from flask import Flask, request

app = Flask(__name__)
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        predictions = model.predict(data['instances'])
        return {'predictions': predictions.tolist()}
    except Exception as e:
        return {'error': str(e)}, 400

app.run(host='0.0.0.0', port=8080)
"""]