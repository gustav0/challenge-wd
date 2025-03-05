import pytest

from app.config.email_service import EmailServiceConfig

from . import email_service_data as data


class TestEmailServiceConfig:

    @pytest.mark.parametrize("data", data.test_config)
    def test_email_config(self, data):
        service_data = {
            data["service"]: data[data["service"]],
        }

        conf = EmailServiceConfig(
            service=data["service"],
            **service_data,
        )

        assert conf.service == data["service"]
        service_config = getattr(conf, conf.service)

        # Check service config values are set
        for key, value in service_data[data["service"]].items():
            assert getattr(service_config, key) == value

    @pytest.mark.parametrize("service", [1, None, "", "invalid"])
    def test_invalid_service(self, service):
        with pytest.raises(ValueError, match="Input should be"):
            EmailServiceConfig(
                service=service,
            )

    def test_missing_service(self):
        with pytest.raises(ValueError, match="Field required"):
            EmailServiceConfig()

    @pytest.mark.parametrize("service", ["sendgrid", "ses"])
    def test_missing_service_config(self, service):
        with pytest.raises(
            ValueError,
            match=f"Email service is set to '{service}' but no config provided",
        ):
            EmailServiceConfig(service=service)
