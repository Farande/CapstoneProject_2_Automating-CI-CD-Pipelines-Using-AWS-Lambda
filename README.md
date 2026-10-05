# Automating CI/CD Pipelines Using AWS Lambda

## Project Overview

This project demonstrates how AWS Lambda can be used to automate a deployment task in a CI/CD pipeline.

A sample static website is stored in a GitHub repository. When changes are pushed to the `main` branch, AWS CodePipeline detects the change and passes the source artifact to an AWS Lambda function.

The Lambda function extracts the application files and deploys them to an Amazon S3 bucket.

The deployment process is monitored using Amazon CloudWatch.

## Objective

The main objective of this project is to demonstrate an event-driven CI/CD workflow using AWS Lambda without using AWS CodeBuild.

The workflow automatically deploys changes from GitHub to an Amazon S3 static website.

## Architecture

Developer
    |
    | git push
    v
GitHub Repository
    |
    | Source
    v
AWS CodePipeline
    |
    | Source Artifact
    v
AWS Lambda
    |
    | Upload Website Files
    v
Amazon S3
    |
    | Static Website
    v
Website Users

AWS Lambda
    |
    v
Amazon CloudWatch
    |
    | Logs
    v
Monitoring

## CI/CD Flow

1. Developer modifies the application.
2. Developer commits the changes.
3. Developer pushes the changes to the GitHub `main` branch.
4. AWS CodePipeline detects the new commit.
5. CodePipeline downloads the source repository.
6. CodePipeline passes the source artifact to the Lambda deployment function.
7. Lambda downloads the artifact.
8. Lambda extracts the application files.
9. Lambda uploads the files to the S3 deployment bucket.
10. Lambda reports the deployment result to CodePipeline.
11. CloudWatch stores the Lambda execution logs.
12. Users can access the updated static website.

## AWS Services Used

### 1. GitHub

GitHub stores the application source code.

The repository contains:

```text

index.html

style.css

README.md

```

### 2. AWS CodePipeline

AWS CodePipeline manages the CI/CD workflow.

It performs the following tasks:

```text

GitHub

&#x20;  |

&#x20;  v

Source Stage

&#x20;  |

&#x20;  v

Lambda Deployment

```

CodeBuild is intentionally not used in this project.

### 3. AWS Lambda

Lambda performs the deployment automation.

The Lambda function:

* Receives the CodePipeline job event.
* Identifies the source artifact.
* Downloads the artifact.
* Extracts the files.
* Uploads the files to Amazon S3.
* Reports success or failure to CodePipeline.

### 4. Amazon S3

Amazon S3 stores the deployed website files.

Example:

```text

S3 Bucket

│

├── index.html

└── style.css

```

The S3 bucket is configured for static website hosting.

### 5. IAM

IAM controls permissions between AWS services.

The CodePipeline service role is allowed to invoke the Lambda function.

The Lambda execution role is allowed to:

* Read the CodePipeline artifact.
* Upload files to S3.
* Delete objects when required.
* Report success to CodePipeline.
* Report failure to CodePipeline.

### 6. CloudWatch

CloudWatch is used to monitor Lambda execution.

Example log messages include:

```text

Lambda deployment started

Artifact downloaded

Artifact extracted

Uploaded: index.html

Uploaded: style.css

Deployment completed

```

If the deployment fails, the error is recorded in CloudWatch Logs.

## Lambda Deployment Logic

The Lambda function follows this process:

Receive CodePipeline Event
          |
          v
Get Source Artifact
          |
          v
Download ZIP Artifact
          |
          v
Extract Files
          |
          v
Upload Files to S3
          |
          v
Deployment Successful?
       /       \
     Yes        No
      |          |
      v          v
CodePipeline   CodePipeline
SUCCESS        FAILURE


## Security Configuration

IAM follows the principle of least privilege.

### CodePipeline Role

The CodePipeline service role requires permission to invoke the deployment Lambda function.

Example permission:

```json

{

&#x20;   "Effect": "Allow",

&#x20;   "Action": \[

&#x20;       "lambda:InvokeFunction"

&#x20;   ],

&#x20;   "Resource": "arn:aws:lambda:ap-south-1:ACCOUNT\_ID:function:LambdaCICDDeploy"

}

```

### Lambda Role

The Lambda execution role requires access to the required S3 objects and CodePipeline result APIs.

Required permissions include:

s3:GetObject
s3:PutObject
s3:DeleteObject
s3:ListBucket
codepipeline:PutJobSuccessResult
codepipeline:PutJobFailureResult


Permissions should be restricted to the required resources where possible.

## Failure Handling

If Lambda encounters an error during deployment, the exception is captured.

Lambda reports the failure to CodePipeline using:


PutJobFailureResult

The deployment stage is then marked as failed.

The failure can be investigated using CloudWatch Logs.

Example:


CodePipeline
     |
     v
Lambda
     |
     X
Deployment Error
     |
     v
PutJobFailureResult
     |
     v
Pipeline Failed
     |
     v
CloudWatch Logs


## Testing

### Test 1 — Initial Deployment

Push the initial application:


git add .
git commit -m "Initial application"
git push origin main


CodePipeline should start automatically.

Expected flow:


GitHub
   ↓
CodePipeline
   ↓
Lambda
   ↓
S3


### Test 2 — Application Update

Modify `index.html`.

For example:


<h1>AWS Lambda CI/CD Pipeline Version 2</h1>


Then run:


git add .
git commit -m "Update website"
git push origin main


CodePipeline should detect the new commit and deploy the updated files.

### Test 3 — Failure

A deployment failure can be tested by temporarily introducing an invalid configuration or permission issue.

Expected behavior:


Lambda Error
     ↓
CloudWatch Logs
     ↓
CodePipeline Deployment Failed


After correcting the configuration, another GitHub push can trigger a new deployment.

## Monitoring

AWS CloudWatch is used to monitor Lambda executions.

Important information includes:

* Invocation count
* Execution duration
* Errors
* Log messages
* Deployment failures

CloudWatch Logs can be opened from:


AWS Console
    ↓
Lambda
    ↓
LambdaCICDDeploy
    ↓
Monitor
    ↓
View CloudWatch Logs


## Why These Services Were Selected

| Service      | Purpose                          |
| ------------ | -------------------------------- |
| GitHub       | Source code management           |
| CodePipeline | CI/CD orchestration              |
| Lambda       | Serverless deployment automation |
| S3           | Static website hosting           |
| IAM          | Access control                   |
| CloudWatch   | Monitoring and logs              |

## Why Lambda Instead of CodeBuild?

This project intentionally does not use CodeBuild.

The application is a simple static website, so a separate build server is not required.

Lambda can directly perform the deployment task:


Source Artifact
      ↓
Lambda
      ↓
S3


This demonstrates how a serverless function can perform an event-driven deployment operation.

## Production Improvements

For a production environment, the following improvements could be considered:

1. Use a private S3 bucket and serve the website through CloudFront.
2. Use HTTPS through CloudFront.
3. Apply least-privilege IAM policies.
4. Enable S3 versioning.
5. Enable CloudTrail for audit logging.
6. Add CloudWatch alarms for Lambda failures.
7. Add deployment notifications.
8. Use separate development, staging, and production environments.
9. Add automated testing before deployment.
10. Add manual approval before production deployment when required.
11. Store sensitive configuration in an appropriate secrets/configuration service.
12. Use infrastructure-as-code such as AWS CloudFormation or Terraform.

## Project Limitations

This project is designed as a learning demonstration.

It does not include:

* AWS CodeBuild
* EC2
* ECS
* ECR
* RDS
* API Gateway

The application is a static website and therefore does not require a backend server or database.

## Expected Result

After a successful deployment:

Developer
    ↓
GitHub
    ↓
CodePipeline
    ↓
Lambda
    ↓
S3
    ↓
Updated Website


The project demonstrates an automated, serverless CI/CD deployment workflow using AWS Lambda.

Image1:CodePipeline Configuration

<img width="1366" height="768" alt="Screenshot (700)" src="https://github.com/user-attachments/assets/b0f6b66a-de22-4463-bae5-cd9f706a4509" />


Image2:CodePipeline Execution

<img width="1366" height="768" alt="Screenshot (703)" src="https://github.com/user-attachments/assets/e3a4e2d4-9f81-419d-bc44-5f2e078c0975" />


Image4:Lambda IAM Role

<img width="1366" height="768" alt="Screenshot (712)" src="https://github.com/user-attachments/assets/c3db2950-b111-48da-b109-b04c4f53899b" />


Image5:CodePipeline IAM role

<img width="1366" height="768" alt="Screenshot (713)" src="https://github.com/user-attachments/assets/aef74c36-f26e-4a61-abde-21fd0e52ad33" />


Image6:S3 bucket

<img width="1366" height="768" alt="Screenshot (698)" src="https://github.com/user-attachments/assets/ebb7cee4-1e31-481c-9713-e8746a0f616e" />


Image7:Running application

<img width="1366" height="768" alt="Screenshot (701)" src="https://github.com/user-attachments/assets/e7b8bf4f-cf3f-445a-9c37-1b975acd7aa6" />


Image8:CloudWatch logs

<img width="1366" height="768" alt="Screenshot (702)" src="https://github.com/user-attachments/assets/6c820b19-1e31-4fb9-86ab-742fb48e32dc" />

Image 9:GitHub repository

<img width="1366" height="768" alt="Screenshot (715)" src="https://github.com/user-attachments/assets/9635b2a8-5d0d-44e7-b2b9-3eef9392e74d" />



