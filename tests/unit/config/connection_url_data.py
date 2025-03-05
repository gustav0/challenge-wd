test_connection_url = [
    {
        "init": {
            "scheme": "redis",
            "host": "localhost",
            "port": 6379,
            "password": "redis",
            "path": "/0",
        },
        "expected": "redis://:redis@localhost:6379/0",
    },
    {
        "init": {
            "scheme": "amqp",
            "host": "localhost",
            "port": 5672,
            "username": "rabs",
            "password": "rabs",
            "path": "/rabs",
        },
        "expected": "amqp://rabs:rabs@localhost:5672/rabs",
    },
    {
        "init": {
            "scheme": "kafka",
            "host": "localhost",
            "port": 9092,
            "path": "/",
            "query": {"topic": "mytopic"},
        },
        "expected": "kafka://localhost:9092/?topic=mytopic",
    },
]
