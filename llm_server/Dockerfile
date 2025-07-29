FROM python:3.10-slim

WORKDIR /app

COPY llm_server/llm_server.py .
COPY llm_server/chat ./chat
COPY llm_server/requirements.txt .
COPY llm_server/inference_pb2.py .
COPY llm_server/inference_pb2_grpc.py .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "./llm_server.py"]
