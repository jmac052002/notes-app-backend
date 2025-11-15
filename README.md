# Serverless Notes App – Backend (AWS Lambda + DynamoDB)

This repo contains the **backend Lambda function** for a simple serverless Notes app
used to practice AWS services for the **AWS Solutions Architect – Associate** exam.

## Architecture (Backend)

- **AWS Lambda** – Python function that handles note operations
- **Amazon DynamoDB** – `notes-app` table
  - Partition key: `userId` (String)
  - Sort key: `noteId` (String)
- **IAM** – execution role with permissions to DynamoDB + CloudWatch Logs

In the current version, the Lambda function:

1. Uses a fixed `userId` (`test-user-123`) for testing
2. Creates a new note item in DynamoDB
3. Reads the item back
4. Returns the saved note in the response

Later, this will be extended to a full CRUD API behind **API Gateway** and protected by **Cognito**.

## Lambda Handler

Main entrypoint: `src/handler.py` → `lambda_handler`.

Environment variable:

- `TABLE_NAME` – name of the DynamoDB table (default: `notes-app`)

## Deploying the Code to Lambda (manual zip upload)

1. From this repo root, create a deployment package:

   ```bash
   cd src
   zip -r ../function.zip .
   cd ..
