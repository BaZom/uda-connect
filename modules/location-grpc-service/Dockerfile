FROM python:3.8

WORKDIR .

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
ENTRYPOINT ["python", "forward-to-kafka.py"]