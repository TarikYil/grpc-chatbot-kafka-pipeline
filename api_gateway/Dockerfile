FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential gcc curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY api_gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY api_gateway /app


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
