import os
import boto3
import pika
import json
from sqlalchemy import create_engine


class OutputHandler:
    def __init__(self, logger):
        """
        Initializes the output handler based on the configured output type.

        Parameters
        ----------
        logger : logging.Logger
            Logger instance for logging output operations.
        """
        self.logger = logger
        self.output_mode = os.getenv("OUTPUT_MODE", "file").lower()

        # RabbitMQ setup
        if self.output_mode == "rabbitmq":
            self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
            self.rabbitmq_queue = os.getenv("OUTPUT_QUEUE_NAME")
            if not self.rabbitmq_queue:
                raise ValueError("OUTPUT_QUEUE_NAME environment variable is required for RabbitMQ.")

        # SQS setup
        elif self.output_mode == "sqs":
            self.sqs_client = boto3.client("sqs", region_name=os.getenv("AWS_REGION"))
            self.sqs_queue_url = self.sqs_client.get_queue_url(QueueName=os.getenv("OUTPUT_QUEUE_NAME"))["QueueUrl"]

        # Database setup
        elif self.output_mode == "database":
            self.db_url = os.getenv("DATABASE_URL")
            if not self.db_url:
                raise ValueError("DATABASE_URL environment variable is required for database output.")
            self.db_engine = create_engine(self.db_url)

    def send_to_rabbitmq(self, data: dict):
        """
        Sends processed data to a RabbitMQ queue.

        Parameters
        ----------
        data : dict
            Processed data to send.
        """
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
            channel = connection.channel()
            channel.queue_declare(queue=self.rabbitmq_queue)
            channel.basic_publish(
                exchange='',
                routing_key=self.rabbitmq_queue,
                body=json.dumps(data),
            )
            self.logger.info("Data sent to RabbitMQ.")
        except Exception as e:
            self.logger.error(f"Failed to send data to RabbitMQ: {e}", exc_info=True)

    def send_to_sqs(self, data: dict):
        """
        Sends processed data to an SQS queue.

        Parameters
        ----------
        data : dict
            Processed data to send.
        """
        try:
            self.sqs_client.send_message(
                QueueUrl=self.sqs_queue_url,
                MessageBody=json.dumps(data),
            )
            self.logger.info("Data sent to SQS.")
        except Exception as e:
            self.logger.error(f"Failed to send data to SQS: {e}", exc_info=True)

    def send_to_database(self, data: dict):
        """
        Inserts processed data into a database.

        Parameters
        ----------
        data : dict
            Processed data to insert.
        """
        try:
            with self.db_engine.connect() as conn:
                conn.execute(
                    "INSERT INTO analysis_results (symbol, analysis_data) VALUES (:symbol, :analysis_data)",
                    {"symbol": data["symbol"], "analysis_data": json.dumps(data["analysis"])},
                )
            self.logger.info("Data inserted into database.")
        except Exception as e:
            self.logger.error(f"Failed to insert data into database: {e}", exc_info=True)

    def save(self, data: dict):
        """
        Sends or saves processed data based on the configured output mode.

        Parameters
        ----------
        data : dict
            Processed data to handle.
        """
        if self.output_mode == "rabbitmq":
            self.send_to_rabbitmq(data)
        elif self.output_mode == "sqs":
            self.send_to_sqs(data)
        elif self.output_mode == "database":
            self.send_to_database(data)
        else:
            self.logger.error(f"Unsupported OUTPUT_MODE: {self.output_mode}")
