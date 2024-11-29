import os
from helpers.queue_handler import process_queue_message

if __name__ == "__main__":
    # Get the queue type (RabbitMQ or SQS) from environment variables
    QUEUE_TYPE = os.getenv("QUEUE_TYPE", "rabbitmq")
    print(f"Starting time-series-analysis application using {QUEUE_TYPE}...")
    process_queue_message()
