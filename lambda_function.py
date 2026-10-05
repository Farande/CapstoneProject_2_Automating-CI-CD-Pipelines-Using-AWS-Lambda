import boto3
import json
import os
import zipfile
import tempfile

s3 = boto3.client("s3")
codepipeline = boto3.client("codepipeline")

DEPLOY_BUCKET = os.environ["DEPLOY_BUCKET"]


def lambda_handler(event, context):

    job_id = event["CodePipeline.job"]["id"]

    try:

        print("Lambda deployment started")

        job_data = event["CodePipeline.job"]["data"]

        input_artifact = job_data["inputArtifacts"][0]

        artifact_location = input_artifact["location"]["s3Location"]

        artifact_bucket = artifact_location["bucketName"]
        artifact_key = artifact_location["objectKey"]

        print("Artifact bucket:", artifact_bucket)
        print("Artifact key:", artifact_key)

        temp_zip = os.path.join(
            tempfile.gettempdir(),
            "artifact.zip"
        )

        extract_dir = os.path.join(
            tempfile.gettempdir(),
            "website"
        )

        os.makedirs(extract_dir, exist_ok=True)

        # Download artifact
        s3.download_file(
            artifact_bucket,
            artifact_key,
            temp_zip
        )

        print("Artifact downloaded")

        # Extract artifact
        with zipfile.ZipFile(temp_zip, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        print("Artifact extracted")

        # Upload files to deployment bucket
        for root, dirs, files in os.walk(extract_dir):

            for file_name in files:

                local_file = os.path.join(root, file_name)

                relative_file = os.path.relpath(
                    local_file,
                    extract_dir
                )

                s3_key = relative_file.replace("\\", "/")

                content_type = "application/octet-stream"

                if file_name.endswith(".html"):
                    content_type = "text/html"

                elif file_name.endswith(".css"):
                    content_type = "text/css"

                elif file_name.endswith(".js"):
                    content_type = "application/javascript"

                s3.upload_file(
                    local_file,
                    DEPLOY_BUCKET,
                    s3_key,
                    ExtraArgs={
                        "ContentType": content_type
                    }
                )

                print(
                    f"Uploaded: {s3_key}"
                )

        print("Deployment completed")

        codepipeline.put_job_success_result(
            jobId=job_id
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                "Deployment successful"
            )
        }

    except Exception as error:

        print(
            "Deployment failed:",
            str(error)
        )

        codepipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                "type": "JobFailed",
                "message": str(error),
                "externalExecutionId": context.aws_request_id
            }
        )

        raise
