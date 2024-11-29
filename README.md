# Time Series Analysis Application

This application performs time-series analysis on stock data retrieved from a RabbitMQ or SQS queue.

## Features

- Polls data from RabbitMQ or SQS queues
- Performs time-series analysis
- Logs processed results

## Environment Variables

The application is configured via environment variables:

- `QUEUE_TYPE`: Choose `rabbitmq` or `sqs`
- `QUEUE_NAME`: Name of the queue
- `RABBITMQ_HOST`: RabbitMQ hostname
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: AWS credentials for SQS

## Usage

1. Build the Docker container:

   ```bash
   docker build -t time-series-analysis .
