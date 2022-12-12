import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc
import json
from kafka import KafkaProducer
import datetime
import os

#TOPIC_NAME = 'locations'
#KAFKA_SERVER = 'localhost:9092'

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

class locationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):

        grpc_data = {
            "person_id": int(request.person_id),
            "longitude": request.longitude,
            "latitude": request.latitude,
        }
        print(grpc_data)
        self.forward_to_kafka(grpc_data)
        
        return location_pb2.LocationMessage(**grpc_data)

    def forward_to_kafka(self,data):
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

        location_data = json.dumps(data).encode('utf-8')
        producer.send(TOPIC_NAME, location_data)
        producer.flush()
        

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(locationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)