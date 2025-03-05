test_config = [
    {
        "engine": "postgres",
        "postgres": {
            "username": "postgres",
            "password": "postgres",
            "db_name": "postgres",
            "host": "localhost",
            "port": 5432,
        },
    },
    {
        "engine": "sqlite",
        "sqlite": {
            "path": ":memory:",
        },
    },
]
