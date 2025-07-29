from fastapi import FastAPI
from routes import router
from fastapi.responses import JSONResponse
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# Include the router
app.include_router(router)

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint to verify the service is running."""
    return JSONResponse(content={"status": "ok"}, status_code=200)


