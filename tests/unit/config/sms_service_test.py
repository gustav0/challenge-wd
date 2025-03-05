import pytest

from app.config.sms_service import SMSServiceConfig

from . import sms_service_data as data


class TestSMSServiceConfig:

    @pytest.mark.parametrize("data", data.test_config)
    def test_sms_config(self, data):
        service_data = {
            data["service"]: data[data["service"]],
        }

        conf = SMSServiceConfig(
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
            SMSServiceConfig(
                service=service,
            )

    def test_missing_service(self):
        with pytest.raises(ValueError, match="Field required"):
            SMSServiceConfig()

    @pytest.mark.parametrize("service", ["sns", "twilio"])
    def test_missing_service_config(self, service):
        with pytest.raises(
            ValueError,
            match=f"SMS service is set to '{service}' but no config provided",
        ):
            SMSServiceConfig(service=service)
