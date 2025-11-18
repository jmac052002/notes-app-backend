📝 Serverless Notes API (AWS Lambda + DynamoDB + API Gateway)

This project is a fully serverless backend that exposes a simple REST API for creating and retrieving “notes.”
It is built using:

AWS Lambda (Python)

Amazon API Gateway – HTTP API

Amazon DynamoDB (NoSQL key–value store)

IAM (Execution roles, least privilege)

CloudWatch Logs (Monitoring + diagnostics)

This is a real cloud-native microservice: scalable, event-driven, fully managed, and designed using AWS best-practice patterns.

🧱 Architecture Overview
                   ┌──────────────────────────────┐
                   │         Client / CLI         │
                   │   curl, browser, Postman     │
                   └──────────────┬───────────────┘
                                  │ HTTPS (REST)
                                  ▼
                     ┌──────────────────────────┐
                     │  Amazon API Gateway      │
                     │  HTTP API (GET /notes    │
                     │             POST /notes) │
                     └──────────────┬───────────┘
                                  │ Lambda proxy integration
                                  ▼
                     ┌──────────────────────────┐
                     │ AWS Lambda Function      │
                     │  handler.py              │
                     └──────────────┬───────────┘
                                  │ boto3 PutItem / Scan
                                  ▼
                     ┌──────────────────────────┐
                     │ Amazon DynamoDB Table    │
                     │  notes-app               │
                     │  PK: noteId (string)     │
                     └──────────────────────────┘

🚀 Features
✔ Create a new note (POST /notes)

Stores:

noteId (UUID)

userId (test-user for now)

title

content

createdAt / updatedAt

✔ Get all notes (GET /notes)

Returns an array of notes stored in DynamoDB.

✔ Fully serverless

No servers to run or manage — infinite horizontal scaling.

✔ Low cost

Typical monthly cost = <$1 unless handling millions of requests.

🛠 Tech Stack
Service	Purpose
AWS Lambda (Python 3.12)	Runs backend compute
API Gateway HTTP API	REST routing + HTTPS endpoint
DynamoDB	NoSQL storage (key–value)
IAM	Secure execution roles
CloudWatch Logs	Debugging / monitoring
📁 Project Structure
notes-app-backend/
│
├── handler.py         # Lambda REST API logic
├── package.json       # (optional) for tooling
├── README.md          # This file
└── ...                # zip uploaded to Lambda

🔐 IAM — Least Privilege Access

The Lambda execution role follows AWS security best practices:

Allowed actions:

{
  "dynamodb:PutItem",
  "dynamodb:Scan"
}


Resource restricted to your specific table ARN only.

This directly aligns with SAA exam principles:

Principle of least privilege

Scoped permissions

Granular DynamoDB table resource ARNs

No wildcards like * for resources

🗄 DynamoDB Table Schema
Attribute	Type	Purpose
noteId	string (PK)	Unique identifier
userId	string	Simulated user for now
title	string	Note title
content	string	Note content
createdAt	string	ISO timestamp
updatedAt	string	ISO timestamp

This table is optimized for:

Fast primary-key access

Serverless workloads

Predictable performance

🧪 Testing the API
✔️ GET all notes
https://YOUR-ID.execute-api.us-east-1.amazonaws.com/notes


Or using curl:

curl https://YOUR-ID.execute-api.us-east-1.amazonaws.com/notes

✔️ POST a new note
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Note","content":"Created via API"}' \
  https://YOUR-ID.execute-api.us-east-1.amazonaws.com/notes

📡 API Endpoints
Method	Path	Description
GET	/notes	Retrieve all notes
POST	/notes	Create a new note

Routing is handled by API Gateway → Lambda Proxy Integration, which passes the entire HTTP request to Lambda.

📈 CloudWatch Monitoring

Each Lambda invocation generates:

Request ID

Duration

Cold start info

Errors and stack traces

You can view logs via:

CloudWatch → Log Groups → /aws/lambda/notes-app-handler

⚙️ How to Deploy (Solutions Architect Level)
✦ 1. Create DynamoDB Table
notes-app (PK: noteId)

✦ 2. Create Lambda Function (Python 3.12)

Upload function.zip.

Set environment variable:

TABLE_NAME=notes-app

✦ 3. Attach IAM Role

Grant:

dynamodb:PutItem

dynamodb:Scan

Scoped to that one table.

✦ 4. Create API Gateway (HTTP API)

Routes:

GET /notes

POST /notes

Integrate both with Lambda.

✦ 5. Deploy Stage $default
✦ 6. Test with browser or curl
📚 Architecture Reasoning (for SAA Exam Readiness)
Why AWS Lambda?

Event-driven

No server management

Cheap

Scales automatically

Perfect for REST APIs without heavy compute

Why DynamoDB vs RDS?

No servers

Instant scaling

Millisecond latency

Pay-per-request pricing

Dynamic schema

Why API Gateway HTTP API (not REST API)?

Lower cost

Lower latency

Built for “Lambda proxy” microservices

Perfect for simple serverless APIs

Why separate GET/POST routes?

API Gateway routing decouples transport from application logic

Cleaner, more scalable than “single Lambda with switch()”

🧭 Scalability Considerations

This architecture supports:

Massive parallel writes (DynamoDB partitions scale automatically)

High read throughput

Lambda concurrency scaling

Fully managed infrastructure

If traffic increases 1000x:

No auto-scaling groups

No containers

No servers

No patching
AWS handles everything.

🔥 Production Enhancement Ideas

These are fantastic talking points for interviews:

Add user authentication via Cognito

Add API Keys + throttling

Add X-Ray tracing

Add CloudFormation or Terraform IaC

Add S3-backed frontend

Add CI/CD pipeline (GitHub Actions → Lambda)

Add DLQ + retries for advanced resilience

🔗 Repository

GitHub repo:

https://github.com/jmac052002/notes-app-backend

📄 License

MIT License
Feel free to use this architecture as a starter for your own AWS projects.
