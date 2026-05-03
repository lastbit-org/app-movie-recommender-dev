import argparse
import uuid
from google.cloud import aiplatform

def submit(project: str, region: str, image: str, model_bucket: str,
           staging_bucket: str, endpoint_id: str):
    aiplatform.init(
        project=project,
        location=region,
        staging_bucket=staging_bucket,
    )

    run_id = uuid.uuid4().hex[:8]

    # 1. treino
    job = aiplatform.CustomContainerTrainingJob(
        display_name=f"movie-recommender-{run_id}",
        container_uri=image,
    )

    job.run(
        args=[
            f"--model-bucket={model_bucket}",
            f"--run-id={run_id}",
        ],
        replica_count=1,
        machine_type="n2-standard-4",
        sync=True,   # aguarda antes de registrar
    )

    # 2. registra no Model Registry
    model = aiplatform.Model.upload(
        display_name=f"movie-recommender-{run_id}",
        artifact_uri=f"gs://{model_bucket}/runs/{run_id}/",
        serving_container_image_uri="us-central1-docker.pkg.dev/lastbit-prj-d-movieapi/reg-d-movieapi-pipelines/serving:latest",
        labels={"env": "dev", "workload": "movieapi"},
    )

    print(f"modelo registrado: {model.resource_name}")

    # 3. deploy no endpoint
    endpoint = aiplatform.Endpoint(endpoint_name=endpoint_id)

    model.deploy(
        endpoint=endpoint,
        machine_type="n2-standard-2",
        min_replica_count=1,
        max_replica_count=2,
        traffic_percentage=100,
        # sync=True,
    )

    print(f"deploy concluído: {endpoint.resource_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project",        required=True)
    parser.add_argument("--region",         required=True)
    parser.add_argument("--image",          required=True)
    parser.add_argument("--model-bucket",   default="bkt-d-movieapi-models")
    parser.add_argument("--staging-bucket", default="gs://bkt-d-movieapi-artifacts")
    parser.add_argument("--endpoint-id",    required=True)
    args = parser.parse_args()

    submit(args.project, args.region, args.image,
           args.model_bucket, args.staging_bucket, args.endpoint_id)
