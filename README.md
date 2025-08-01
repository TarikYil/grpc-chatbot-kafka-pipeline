# gRPC LLM Service

## Overview
This project is a gRPC-based service designed to handle language model requests. It consists of an API Gateway, an LLM Client, and an LLM Server. The system uses Kafka for message brokering between components.

## Project Structure
- **api_gateway/**: Contains the FastAPI application that serves as the API Gateway.
- **llm_client/**: A Go-based client that communicates with the LLM Server via gRPC.
- **llm_server/**: The gRPC server that processes language model requests.
- **proto/**: Contains the gRPC protocol buffer definitions.

## Architecture
1. **API Gateway (FastAPI)**:
   - Receives HTTP requests and sends them as messages to Kafka.
   - The `/predict` endpoint accepts a `prompt` from the user and sends it to Kafka.

2. **LLM Client (Go)**:
   - Listens to the `prompt-requests` topic on Kafka and retrieves incoming requests.
   - Sends these requests to the LLM Server using gRPC.
   - Receives responses from the LLM Server and sends them back to Kafka on the `prompt-responses` topic.

3. **LLM Server (Python, gRPC)**:
   - Processes requests received via gRPC.
   - Uses `VoiceChatBot` to generate a response for the `prompt`.
   - Sends the response back to the client via gRPC.

4. **Kafka**:
   - Acts as a broker for message exchange.
   - The API Gateway sends requests to the `prompt-requests` topic.
   - The LLM Client retrieves requests from this topic, processes them, and sends responses to the `prompt-responses` topic.
   - The API Gateway retrieves responses from this topic and delivers them to the user.

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose
- Go (for building the client)
- Python 3.8+

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd grpc-llm-service
   ```

2. Build and start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. The API Gateway will be available at `http://localhost:8000`.

## Usage

### API Gateway
- **Endpoint**: `/predict`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "prompt": "Your prompt here"
  }
  ```
- **Response**:
  - Success: `{ "result": "response from model" }`
  - Timeout/Error: `{ "error": "timeout" }`

### Health Check
- **Endpoint**: `/health`
- **Method**: GET
- **Response**: `{ "status": "ok" }`

## Development

### Running Locally
- Ensure Kafka is running and accessible at `kafka:9092`.
- Use `uvicorn` to run the API Gateway:
  ```bash
  uvicorn api_gateway.main:app --reload
  ```

### Testing
- Use tools like `curl` or Postman to test the API endpoints.

## Contributing
Feel free to open issues or submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.
