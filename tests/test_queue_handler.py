from unittest.mock import MagicMock, patch
from app.queue_handler import QueueHandler


def test_poll_sqs():
    """Test polling messages from SQS."""
    mock_logger = MagicMock()
    handler = QueueHandler(mock_logger)
    handler.queue_type = "SQS"
    handler.queue_name = "test_sqs_queue"

    with patch("boto3.client") as mock_boto:
        mock_boto.return_value.receive_message.return_value = {
            "Messages": [{"Body": "test_message", "ReceiptHandle": "abc123"}]
        }
        messages = list(handler.poll_sqs())
        assert len(messages) == 1
        assert messages[0] == "test_message"
        mock_logger.info.assert_any_call("SQS message deleted.")


def test_poll_rabbitmq():
    """Test polling messages from RabbitMQ."""
    mock_logger = MagicMock()
    handler = QueueHandler(mock_logger)
    handler.queue_type = "RABBITMQ"
    handler.queue_name = "test_rabbitmq_queue"

    with patch("pika.BlockingConnection") as mock_connection:
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        mock_channel.consume.return_value = [
            (MagicMock(), MagicMock(), b"test_message")
        ]
        messages = list(handler.poll_rabbitmq())
        assert len(messages) == 1
        assert messages[0] == "test_message"
        mock_logger.info.assert_called_with("RabbitMQ message acknowledged.")
