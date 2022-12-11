import grpc
import location_pb2
import location_pb2_grpc
import datetime

"""
Sample implementation of a location generator that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = location_pb2.LocationMessage(
    person_id=1,
    longitude="-122.290883",
    latitude="37.55363",
)


response = stub.Create(location)