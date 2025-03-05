# This is simulating external API calls from the service
async def mock_sendgrid_api_call(
    to_email: str,
    subject: str,
    body: str,
) -> bool:
    """Simulate SendGrid API call. This could be imported from the SendGrid SDK."""
    return True  # pragma: no cover


async def mock_ses_api_call(
    to_email: str,
    subject: str,
    body: str,
) -> bool:
    """Simulate AWS SES API call. Again, could be imported from boto3 or any other AWS SES SDK / wrapper."""
    return True  # pragma: no cover
