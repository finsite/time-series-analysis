import os

import boto3
import pika
from botocore.exceptions import BotoCoreError, ClientError


class QueueHandler:
    def __init__(self, logger):
        self.logger = logger
        self.queue_type = os.getenv("QUEUE_TYPE", "SQS").upper()
        self.queue_name = os.getenv("QUEUE_NAME")
        if not self.queue_name:
            raise ValueError("QUEUE_NAME environment variable is required.")

    def poll_sqs(self):
        """
        Poll messages from an SQS queue.

        Yields
        ------
        str
            The body of each message received from the SQS queue.
        """
        try:
            session = boto3.session.Session()
            sqs = session.client("sqs", region_name=os.getenv("AWS_REGION"))
            queue_url = sqs.get_queue_url(QueueName=self.queue_name)["QueueUrl"]

            while True:
                response = sqs.receive_message(
                    QueueUrl=queue_url,
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=10,
                )
                messages = response.get("Messages", [])
                if not messages:
                    self.logger.info("No messages in SQS queue.")
                    continue

                for message in messages:
                    yield message["Body"]
                    sqs.delete_message(
                        QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
                    )
                    self.logger.info("SQS message deleted.")

        except (BotoCoreError, ClientError) as e:
            self.logger.error(f"SQS error: {e}", exc_info=True)

    def poll_rabbitmq(self):
        """
        Poll messages from a RabbitMQ queue.

        Yields
        ------
        str
            The body of each message received from the RabbitMQ queue.
        """
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "localhost"))
            )
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name)

            for method_frame, properties, body in channel.consume(self.queue_name):
                yield body.decode()
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                self.logger.info("RabbitMQ message acknowledged.")
        except Exception as e:
            self.logger.error(f"RabbitMQ error: {e}", exc_info=True)

    def poll(self):
        """
        Poll messages from the configured queue.

        This method polls messages from the specified queue based on the
        configured queue type. If the queue type is SQS, this method uses the
        Boto3 library to interact with the Amazon SQS service. If the queue type
        is RabbitMQ, this method uses the Pika library to interact with the
        RabbitMQ message broker.

        Yields
        ------
        str
            The body of each message received from the specified queue.
        """
        if self.queue_type == "SQS":
            return self.poll_sqs()
        elif self.queue_type == "RABBITMQ":
            return self.poll_rabbitmq()
        else:
            self.logger.error(f"Unsupported queue type: {self.queue_type}")
            return iter([])