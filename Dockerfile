FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir scikit-learn flask google-cloud-storage

COPY app.py .
COPY model.pkl .

EXPOSE 8080

CMD ["python", "app.py"]