test_send_email = [
    {
        "id": "sent_false",
        "init": {
            "api_key": "test-api-key",
            "from_email": "from-email@example.com",
            "to_email": "test.1@example.com",
            "subject": "This is a test!",
            "body": "Hey use regular letters",
        },
        "expected": True,
    },
    {
        "id": "sent_true",
        "init": {
            "api_key": "test-api-key-2",
            "from_email": "from-email-2@example.com",
            "to_email": "test.2@example.com",
            "subject": "This is also a test",
            "body": "But we should also use some uncommon characters. Like áéíóúñ",
        },
        "expected": False,
    },
]
