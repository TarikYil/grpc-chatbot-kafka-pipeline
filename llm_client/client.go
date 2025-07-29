package main

import (
    "context"
    "encoding/json"
    "log"
    "time"

    "github.com/segmentio/kafka-go"
    "google.golang.org/grpc"
    pb "grpc-llm-service/proto"
)

type RequestMsg struct {
    RequestID string `json:"request_id"`
    Prompt    string `json:"prompt"`
}

type ResponseMsg struct {
    RequestID string `json:"request_id"`
    Response  string `json:"response"`
}

func main() {
    consumer := kafka.NewReader(kafka.ReaderConfig{
        Brokers: []string{"kafka:9092"},
        Topic:   "prompt-requests",
        GroupID: "go-worker",
    })

    producer := kafka.NewWriter(kafka.WriterConfig{
        Brokers: []string{"kafka:9092"},
        Topic:   "prompt-responses",
    })

    for {
        m, _ := consumer.ReadMessage(context.Background())
        var req RequestMsg
        json.Unmarshal(m.Value, &req)

        conn, _ := grpc.Dial("llm-server:50051", grpc.WithInsecure())
        client := pb.NewInferenceServiceClient(conn)

        ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
        res, err := client.Inference(ctx, &pb.InferenceRequest{Prompt: req.Prompt})
        cancel()
        conn.Close()

        if err != nil {
            log.Println("gRPC hata:", err)
            continue
        }

        resp := ResponseMsg{RequestID: req.RequestID, Response: res.Response}
        val, _ := json.Marshal(resp)
        producer.WriteMessages(context.Background(), kafka.Message{Value: val})
    }
}
