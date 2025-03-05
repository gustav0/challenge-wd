import pytest

from app.config.utils import ConnectionURL

from . import connection_url_data as data


@pytest.mark.parametrize("data", data.test_connection_url)
def test_connection_url(data):
    init_params = data["init"]
    expected_url = data["expected"]
    url = ConnectionURL(**init_params)
    assert str(url) == expected_url
