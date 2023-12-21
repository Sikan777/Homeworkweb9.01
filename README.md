<<<<<<< HEAD
# Homework 8.01: MongoDB, RabbitMQ, and Redis

## Introduction

# Homework 8.01: MongoDB, RabbitMQ, and Redis

## Introduction

This project focuses on integrating MongoDB Atlas for cloud-based data storage, RabbitMQ for message queuing, and Redis for caching. The task is divided into two main parts:

...

### Installation and Dependencies

Before running the scripts, ensure you have the following components installed and configured:

#### MongoDB Atlas

1. Set up a cloud-based MongoDB instance on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Obtain the connection details.

#### RabbitMQ

1. Install RabbitMQ locally or set it up on a server. Refer to the [official installation guide](https://www.rabbitmq.com/download.html).
2. Configure RabbitMQ credentials.

#### Redis

1. Install and configure Redis locally. Follow the instructions [here](https://redis.io/download).

#### Python Packages

Install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. **Start MongoDB and RabbitMQ services.**

2. **Run the data loading scripts for MongoDB:**

    ```bash
    python load_mongo.py
    ```

3. **Run the search script for MongoDB:**

    ```bash
    python search_quotes.py
    ```

4. **Run the producer script for RabbitMQ:**

    ```bash
    python producer.py
    ```

5. **Run the consumer script for RabbitMQ:**

    ```bash
    python consumer.py
    ```

...

## Additional Features (Optional)

### Shortened Commands

In the search script, you can use shortened commands for user convenience:

- `name:st` for `name:Steve Martin`
- `tag:li` for `tag:life`

### Caching with Redis

To enable caching of search results using Redis, uncomment the relevant sections in the search script (`search_quotes.py`). Ensure that Redis is running before executing the script.


