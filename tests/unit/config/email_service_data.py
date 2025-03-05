test_config = [
    {
        "service": "sendgrid",
        "sendgrid": {
            "api_key": "test_api_key",
            "from_email": "test@sendgrid.com",
        },
    },
    {
        "service": "ses",
        "ses": {
            "region": "aws_region",
            "access_key_id": "test_access_key",
            "secret_access_key": "test_secret_key",
            "from_email": "test@ses.com",
        },
    },
]
