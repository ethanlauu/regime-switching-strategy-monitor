import json
from mangum import Mangum
from .api import app

# Create Mangum handler for AWS Lambda
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    Args:
        event: Lambda event object.
        context: Lambda context object.
    Returns:
        dict: API Gateway response.
    """
    try:
        # Process the event through Mangum
        response = handler(event, context)
        return response
    except Exception as e:
        # Return error response
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
            },
            "body": json.dumps({
                "error": "Internal server error",
                "message": str(e)
            })
        } 