import json
from typing import Any, Dict
import boto3

lambda_client = boto3.client("lambda")
lambda_function_name = "fetch-user-match-history-S3"

def fetch_matches_from_s3(riot_id: str, region: str, year: int, role: str, max_out: int) -> Dict[str, Any]:
    """
    Fetch user matches via Lambda function.
    Lambda function get prepared data from S3 and returns match data.
    """
    payload = {
        "riotId": riot_id,
        "region": region,
        "year": year,
        "role": role,
        "max": max_out,
    }

    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload).encode("utf-8"),
    )

    raw = response["Payload"].read().decode("utf-8", "ignore")
    doc = json.loads(raw)
    body = doc.get("body")
    return body

if __name__ == "__main__":
    fetch_matches_from_s3("Lagusa#JP1", "jp1", 2025, "AUTO", 20)