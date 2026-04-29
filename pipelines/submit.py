import argparse
from google.cloud import aiplatform


def submit(project: str, region: str, image: str, model_bucket: str):
    aiplatform.init(project=project, location=region)

    job = aiplatform.CustomContainerTrainingJob(
        display_name="movie-recommender",
        container_uri=image,
    )

    job.run(
        args=[
            f"--model-bucket={model_bucket}",
            f"--run-id={job.display_name}",
        ],
        replica_count=1,
        machine_type="n2-standard-4",
        sync=False,
    )

    print(f"job submetido: {job.resource_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project",      required=True)
    parser.add_argument("--region",       required=True)
    parser.add_argument("--image",        required=True)
    parser.add_argument("--model-bucket", default="bkt-d-movieapi-models")
    args = parser.parse_args()

    submit(args.project, args.region, args.image, args.model_bucket)
