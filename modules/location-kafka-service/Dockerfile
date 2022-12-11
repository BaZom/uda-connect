FROM python:3.8

WORKDIR .

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "kafka-location-consumer.py"]