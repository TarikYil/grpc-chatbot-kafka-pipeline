FROM golang:1.23


WORKDIR /app


COPY go.mod ./
COPY go.sum ./  


COPY llm_client/ ./llm_client/
COPY proto/ ./proto/


WORKDIR /app/llm_client

CMD ["go", "run", "client.go"]
