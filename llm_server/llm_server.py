# import grpc
# from concurrent import futures
# import inference_pb2
# import inference_pb2_grpc
# import time
# import logging
# import json
# from kafka import KafkaConsumer, KafkaProducer
# import threading

# # ChatBot içeri
# try:
#     from chat.chat import VoiceChatBot
# except ImportError:
#     import sys
#     import os
#     sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     from chat.chat import VoiceChatBot

# KAFKA_BROKER = "kafka:9092"
# REQUEST_TOPIC = "prompt-requests"
# RESPONSE_TOPIC = "prompt-responses"

# # Kafka üretici
# producer = KafkaProducer(
#     bootstrap_servers=KAFKA_BROKER,
#     value_serializer=lambda v: json.dumps(v).encode("utf-8")
# )

# class InferenceService(inference_pb2_grpc.InferenceServiceServicer):
#     def __init__(self):
#         try:
#             self.chat_bot = VoiceChatBot()
#             print("VoiceChatBot initialized successfully")
#         except Exception as e:
#             logging.error(f"Failed to initialize VoiceChatBot: {e}")
#             self.chat_bot = None

#     def Inference(self, request, context):
#         prompt = request.prompt
#         request_id = str(int(time.time() * 1000))  # zaman damgasına dayalı örnek ID

#         print(f"[gRPC] Received prompt: {prompt} (id: {request_id})")

#         if self.chat_bot is None:
#             response_text = "ChatBot not available"
#         else:
#             try:
#                 result = self.chat_bot.get_response(prompt)
#                 response_text = result if result else "Empty result from chatbot"
#             except Exception as e:
#                 response_text = f"Error during inference: {str(e)}"

#         # Kafka'ya da gönder (opsiyonel)
#         payload = {"request_id": request_id, "response": response_text}
#         producer.send(RESPONSE_TOPIC, payload)
#         producer.flush()

#         print(f"[gRPC] Returning response: {response_text}")
#         return inference_pb2.InferenceResponse(response=response_text)

#     def process_prompt(self, prompt, request_id):
#         if self.chat_bot is None:
#             response = "ChatBot not available"
#         else:
#             try:
#                 result = self.chat_bot.get_response(prompt)
#                 response = result if result else "Empty result from chatbot"
#             except Exception as e:
#                 response = f"Error during inference: {str(e)}"
        
#         # Yanıtı Kafka'ya gönder
#         payload = {"request_id": request_id, "response": response}
#         producer.send(RESPONSE_TOPIC, payload)
#         producer.flush()
#         print(f"[Kafka] Sent response for {request_id}: {response}")

# def consume_requests(inference_service):
#     consumer = KafkaConsumer(
#         REQUEST_TOPIC,
#         bootstrap_servers=KAFKA_BROKER,
#         group_id="grpc-server-group",
#         value_deserializer=lambda m: json.loads(m.decode("utf-8")),
#         auto_offset_reset='earliest',
#         enable_auto_commit=True
#     )
#     print("[Kafka] Listening for incoming prompts...")

#     for msg in consumer:
#         value = msg.value
#         prompt = value.get("prompt")
#         request_id = value.get("request_id")
#         print(f"[Kafka] Received prompt: {prompt} (id: {request_id})")

#         inference_service.process_prompt(prompt, request_id)

# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     inference_service = InferenceService()
#     inference_pb2_grpc.add_InferenceServiceServicer_to_server(inference_service, server)

#     server.add_insecure_port('[::]:50051')
#     server.start()
#     print("gRPC server started on port 50051")

#     # Kafka thread başlat
#     threading.Thread(target=consume_requests, args=(inference_service,), daemon=True).start()

#     try:
#         server.wait_for_termination()
#     except KeyboardInterrupt:
#         print("Server shutting down...")
#         server.stop(0)

# if __name__ == "__main__":
#     serve()
import grpc
from concurrent import futures
import inference_pb2
import inference_pb2_grpc
import time
import logging
import logging
import sys
import grpc
from concurrent import futures
import time
import logging
import sys


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Import ChatBot
try:
    from chat.chat import VoiceChatBot
except ImportError:
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from chat.chat import VoiceChatBot

class InferenceService(inference_pb2_grpc.InferenceServiceServicer):
    def __init__(self):
        try:
            self.chat_bot = VoiceChatBot()
            logging.info("VoiceChatBot initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize VoiceChatBot: {e}")
            self.chat_bot = None

    def Inference(self, request, context):
        prompt = request.prompt
        request_id = str(int(time.time() * 1000))

        logging.info(f"[gRPC] Received prompt: {prompt} (id: {request_id})")

        if self.chat_bot is None:
            response_text = "ChatBot not available"
            logging.warning("VoiceChatBot is not initialized.")
        else:
            try:
                logging.info("Generating response from chatbot...")
                result = self.chat_bot.get_response(prompt)
                response_text = result if result else "Empty result from chatbot"
                logging.info(f"ChatBot response generated: {response_text}")
            except Exception as e:
                response_text = f"Error during inference: {str(e)}"
                logging.error(f"Exception during get_response: {e}")

        logging.info(f"[gRPC] Returning response: {response_text}")
        return inference_pb2.InferenceResponse(response=response_text)

def serve():
    logging.info("Starting gRPC server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inference_service = InferenceService()
    inference_pb2_grpc.add_InferenceServiceServicer_to_server(inference_service, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("gRPC server started and listening on port 50051")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("Server shutting down...")
        server.stop(0)


if __name__ == "__main__":
    serve()
