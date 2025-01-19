import base64
import json

from google.cloud import pubsub_v1
from celery import shared_task

from core.constants import PROJECT_ID, SUBSCRIPTION_ID
from sensor.serializers import SensorRecordSerializer

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

@shared_task
def process_sensor_data(message):
    try:
        data = json.loads(message.data.decode('utf-8'))
        decoded_data = base64.b64decode(data["message"]["data"]).decode(
            "utf-8"
        )
        sensor_data = json.loads(decoded_data)

        serializer = SensorRecordSerializer(
            data={
                "sensor_id": sensor_data["v0"],
                "human_presence": bool(sensor_data["v11"]),
                "dwell_time": sensor_data["v18"],
                "timestamp": sensor_data["Time"],
            }
        )
        if serializer.is_valid():
            serializer.save()
            message.ack()
        else:
            print(f"Invalid data: {serializer.errors}")
            message.nack()


    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()

def start_subscriber():
    streaming_pull = subscriber.subscribe(subscription_path, callback=process_sensor_data)
    print(f"Started subscribing to {subscription_path}")

    with subscriber:
        try:
            streaming_pull.result()
        except TimeoutError:
            streaming_pull.cancel()