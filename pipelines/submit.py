import argparse
import uuid
from google.cloud import aiplatform


def submit(project: str, region: str, image: str, model_bucket: str, staging_bucket: str):
    aiplatform.init(
        project=project,
        location=region,
        staging_bucket=staging_bucket,
    )

    run_id = uuid.uuid4().hex[:8]   # ← gera antes do job

    job = aiplatform.CustomContainerTrainingJob(
        display_name=f"movie-recommender-{run_id}",
        container_uri=image,
    )

    job.run(
        args=[
            f"--model-bucket={model_bucket}",
            f"--run-id={run_id}",           # ← usa a variável local
        ],
        replica_count=1,
        machine_type="n2-standard-4",
        sync=False,
    )

    print(f"job submetido: movie-recommender-{run_id}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project",      required=True)
    parser.add_argument("--region",       required=True)
    parser.add_argument("--image",        required=True)
    parser.add_argument("--model-bucket", default="bkt-d-movieapi-models")
    parser.add_argument("--staging-bucket", default="gs://bkt-d-movieapi-artifacts")
    args = parser.parse_args()

    submit(args.project, args.region, args.image, args.model_bucket, args.staging_bucket)
