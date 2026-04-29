import argparse
import pickle
import uuid
import numpy as np
from google.cloud import storage


def train(model_bucket: str, run_id: str):
    # dados sintéticos — trocar por leitura do BigQuery depois
    np.random.seed(42)
    n_users, n_movies = 1000, 500
    ratings = np.random.rand(n_users, n_movies)

    # modelo simples: score médio por filme
    movie_scores = ratings.mean(axis=0)
    model = {"movie_scores": movie_scores, "run_id": run_id}

    model_path = "/tmp/model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    client = storage.Client()
    blob = client.bucket(model_bucket).blob(f"runs/{run_id}/model.pkl")
    blob.upload_from_filename(model_path)

    print(f"modelo salvo em gs://{model_bucket}/runs/{run_id}/model.pkl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-bucket", required=True)
    parser.add_argument("--run-id",       required=True)
    args = parser.parse_args()

    train(args.model_bucket, args.run_id)
