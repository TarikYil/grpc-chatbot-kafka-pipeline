# api_gateway/routes.py

from fastapi import APIRouter
from pydantic_model import PromptRequest
import uuid
import threading
from helpers import create_kafka_producer, consume_responses

router = APIRouter()
producer = create_kafka_producer()
responses = {}



# Start Kafka listener in the background
threading.Thread(target=consume_responses, args=(responses,), daemon=True).start()

@router.post("/predict")
def predict(req: PromptRequest):
    """Handle prediction requests and return responses.

    Args:
        req (PromptRequest): The request containing the prompt.

    Returns:
        dict: The result of the prediction or an error message if timed out.
    """
    req_id = str(uuid.uuid4())
    payload = {"request_id": req_id, "prompt": req.prompt}
    producer.send("prompt-requests", payload)
    producer.flush()

    # Wait for a response with simple polling for up to 10 seconds
    for _ in range(20):
        if req_id in responses:
            result = responses.pop(req_id)
            return {"result": result}
        import time
        time.sleep(0.5)

    return {"error": "timeout"}