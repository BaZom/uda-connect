from kafka import KafkaConsumer
import json
import psycopg2
import os
from geoalchemy2.functions import ST_AsText, ST_Point
import datetime



# defined in deployment
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]


consumer = KafkaConsumer(TOPIC_NAME)
for message in consumer:
    decoded_kafka_meassage = message.value.decode('utf-8')
    location_dict = json.loads(decoded_kafka_meassage)

    print(location_dict['longitude'])


    conn = psycopg2.connect(host=DB_HOST,
                            port=DB_PORT,
                            user=DB_USERNAME,
                            password=DB_HOST,
                            database=DB_NAME)

    cursor = conn.cursor()
    cursor.execute(f"insert into public.location (person_id, coordinate, creation_time) values ({location_dict['longitude']}, {ST_Point(location['latitude'], location['longitude'])}, {datetime.datetime.now()})")
    conn.commit()
    cursor.close()
    conn.close()

