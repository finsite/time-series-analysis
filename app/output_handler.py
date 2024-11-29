import json
import os

import boto3
import pika
import psycopg2


class OutputHandler:
    def __init__(self, logger):
        """
        Initialize the OutputHandler class.

        Parameters
        ----------
        logger : Logger
            The logger instance to use for logging.
        """
        self.logger = logger
        # Get the output type from the environment variable
        self.output_type = os.getenv("OUTPUT_TYPE", "SQS").upper()
        # Get the output queue name from the environment variable
        self.output_queue_name = os.getenv("OUTPUT_QUEUE_NAME")

    def output(self, message):
        """
        Handle output based on configuration.

        Parameters
        ----------
        message : str
            The message to be sent to the output queue.
        """
        # Check the output type and send to the appropriate output
        if self.output_type == "SQS":
            # Send the message to an SQS queue
            self.send_to_sqs(message)
        elif self.output_type == "RABBITMQ":
            # Send the message to a RabbitMQ queue
            self.send_to_rabbitmq(message)
        elif self.output_type == "DATABASE":
            # Save the message to a database
            self.save_to_db(message)
        else:
            # If the output type is not supported, log an error
            self.logger.error(f"Unsupported output type: {self.output_type}")

    def send_to_sqs(self, message):
        """
        Send a message to an SQS queue.

        Parameters
        ----------
        message : str
            The message to be sent to the output queue.
        """
        try:
            # Create an SQS client
            session = boto3.session.Session()
            sqs = session.client("sqs", region_name=os.getenv("AWS_REGION"))
            # Get the queue URL
            queue_url = sqs.get_queue_url(QueueName=self.output_queue_name)["QueueUrl"]
            # Send the message to the queue
            sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
            self.logger.info("Message sent to SQS.")
        except Exception as e:
            self.logger.error(f"Error sending to SQS: {e}", exc_info=True)

    def send_to_rabbitmq(self, message):
        """
        Send a message to a RabbitMQ queue.
        """
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "localhost"))
            )
            channel = connection.channel()
            channel.queue_declare(queue=self.output_queue_name)
            channel.basic_publish(
                exchange="",
                routing_key=self.output_queue_name,
                body=json.dumps(message),
            )
            self.logger.info("Message sent to RabbitMQ.")
        except Exception as e:
            self.logger.error(f"Error sending to RabbitMQ: {e}", exc_info=True)

    def save_to_db(self, message):
        """
        Save a message to a database.
        """
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "time_series"),
                user=os.getenv("DB_USER", "user"),
                password=os.getenv("DB_PASSWORD", "password"),
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO analysis_results (symbol, result) VALUES (%s, %s)",
                (message["symbol"], json.dumps(message)),
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.logger.info("Message saved to database.")
        except Exception as e:
            self.logger.error(f"Error saving to database: {e}", exc_info=True)
