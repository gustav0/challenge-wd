test_send_email = [
    {
        "id": "sent_true",
        "init": {
            "region": "aws-region-true",
            "access_key_id": "my-test-access-key-id-true",
            "secret_access_key": "my-test-secret-access-key-true",
            "from_email": "from-email-true@example.com",
            "to_email": "test.1.true@example.com",
            "subject": "This is a test!",
            "body": "Hey use regular letters",
        },
        "expected": True,
    },
    {
        "id": "sent_true",
        "init": {
            "region": "aws-region-false",
            "access_key_id": "my-test-access-key-id-false",
            "secret_access_key": "my-test-secret-access-key-false",
            "from_email": "from-email-false@example.com",
            "to_email": "test.2.false@example.com",
            "subject": "This is also a test",
            "body": "But we should also use some uncommon characters. Like áéíóúñ",
        },
        "expected": False,
    },
]
