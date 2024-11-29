from unittest.mock import MagicMock, patch
from app.output_handler import OutputHandler


def test_send_to_rabbitmq():
    """Test sending data to RabbitMQ."""
    mock_logger = MagicMock()
    handler = OutputHandler(mock_logger)
    handler.rabbitmq_host = "localhost"
    handler.rabbitmq_queue = "test_queue"

    with patch("pika.BlockingConnection") as mock_connection:
        handler.send_to_rabbitmq({"test": "data"})
        mock_logger.info.assert_called_with("Data sent to RabbitMQ.")


def test_send_to_sqs():
    """Test sending data to SQS."""
    mock_logger = MagicMock()
    handler = OutputHandler(mock_logger)
    handler.sqs_queue_url = "https://sqs.us-east-1.amazonaws.com/123456789012/test_queue"

    with patch("boto3.client") as mock_boto:
        handler.send_to_sqs({"test": "data"})
        mock_logger.info.assert_called_with("Data sent to SQS.")


def test_send_to_database():
    """Test sending data to a database."""
    mock_logger = MagicMock()
    handler = OutputHandler(mock_logger)
    handler.db_engine = MagicMock()

    handler.send_to_database({"symbol": "AAPL", "analysis": {"key": "value"}})
    handler.db_engine.connect.assert_called_once()
    mock_logger.info.assert_called_with("Data inserted into database.")
