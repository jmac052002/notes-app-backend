import json
import os
import uuid
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key

# DynamoDB setup
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TABLE_NAME", "notes-app")
table = dynamodb.Table(TABLE_NAME)


def _response(status_code, body):
    """Standard JSON HTTP response."""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def _get_user_id(event):
    """
    Get the userId for the request.

    - Later this will come from Cognito JWT claims.
    - For now:
        * If event["userId"] exists, use that (useful for testing)
        * Otherwise default to "test-user-123"
    """
    # Future: Cognito JWT
    try:
        claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
        return claims.get("sub", "test-user-123")
    except Exception:
        pass

    # Lambda console testing
    user_id = event.get("userId")
    if user_id:
        return user_id

    # Default
    return "test-user-123"


def _list_notes(user_id):
    """GET /notes – list all notes for a user."""
    resp = table.query(
        KeyConditionExpression=Key("userId").eq(user_id)
    )
    items = resp.get("Items", [])
    return _response(200, {"items": items})


def _create_note(user_id, body_dict):
    """POST /notes – create a new note."""
    title = body_dict.get("title", "Untitled")
    content = body_dict.get("content", "")

    note_id = str(uuid.uuid4())
    now_iso = datetime.utcnow().isoformat() + "Z"

    item = {
        "userId": user_id,
        "noteId": note_id,
        "title": title,
        "content": content,
        "createdAt": now_iso,
        "updatedAt": now_iso,
    }

    table.put_item(Item=item)
    return _response(201, {"message": "Note created", "note": item})


def lambda_handler(event, context):
    """
    Main Lambda handler.

    Supports:
      1) Lambda console test events (no routeKey/method):
         -> creates a single test note.

      2) HTTP API v2-style events:
         - GET /notes  -> list notes
         - POST /notes -> create a note from JSON body

    This lets us test now and plug into API Gateway later without code changes.
    """

    # Detect HTTP API v2 fields (what API Gateway will send later)
    route_key = event.get("routeKey")           # e.g. "GET /notes"
    request_context = event.get("requestContext", {})
    http_info = request_context.get("http", {})
    method = http_info.get("method")            # e.g. "GET", "POST"
    raw_path = event.get("rawPath")             # e.g. "/notes"

    user_id = _get_user_id(event)

    # ---------- Case 1: plain Lambda console test ----------
    if not route_key and not method:
        # Simple test: create a note and return it
        test_note_body = {
            "title": "Hello from Lambda (test event)",
            "content": "This note was created when invoking the function from the Lambda console.",
        }
        return _create_note(user_id, test_note_body)

    # ---------- Case 2: HTTP API-style event ----------
    # HTTP API v2 gives routeKey like "GET /notes" or "POST /notes"
    if route_key:
        # GET /notes -> list notes
        if route_key.startswith("GET /notes"):
            return _list_notes(user_id)

        # POST /notes -> create note
        if route_key.startswith("POST /notes"):
            try:
                body_raw = event.get("body") or "{}"
                body_dict = json.loads(body_raw)
            except json.JSONDecodeError:
                return _response(400, {"error": "Invalid JSON body"})

            return _create_note(user_id, body_dict)

    # Anything else: unsupported for now
    return _response(
        400,
        {
            "error": "Unsupported route or method",
            "routeKey": route_key,
            "method": method,
            "path": raw_path,
        },
    )
