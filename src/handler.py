import json
import os
import uuid
from datetime import datetime

import boto3

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TABLE_NAME", "notes-app")
table = dynamodb.Table(TABLE_NAME)


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    """
    Basic handler for now.

    - If called with no specific path/method, it will:
      * Create a test note for user `test-user-123`
      * Read it back and return it

    Later we'll expand this to handle:
      - GET /notes
      - POST /notes
      - PUT /notes/{id}
      - DELETE /notes/{id}
    using API Gateway HTTP API.
    """

    # For now, use a fixed userId. Once Cognito is wired up,
    # we'll extract the real userId from the JWT claims.
    user_id = "test-user-123"

    note_id = str(uuid.uuid4())
    now_iso = datetime.utcnow().isoformat() + "Z"

    item = {
        "userId": user_id,
        "noteId": note_id,
        "title": "Hello from Lambda (Git-backed)",
        "content": "This note was created by the code in your GitHub repo.",
        "createdAt": now_iso,
        "updatedAt": now_iso,
    }

    # Write to DynamoDB
    table.put_item(Item=item)

    # Read it back
    resp = table.get_item(Key={"userId": user_id, "noteId": note_id})
    saved = resp.get("Item", {})

    return _response(200, {"message": "Note saved!", "note": saved})
