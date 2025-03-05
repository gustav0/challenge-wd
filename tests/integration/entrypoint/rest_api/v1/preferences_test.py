import logging

import pytest
from fastapi.testclient import TestClient

from app.domain.schemas import Preferences, User
from app.entrypoint.rest_api.dependencies import (
    get_preferences_repository,
    get_user_repository,
)
from app.entrypoint.rest_api.main import app
from app.ports.preferences_repository import PreferencesRepository
from app.ports.user_repository import UserRepository

logger = logging.getLogger(__name__)


class TestPreferences:
    @pytest.fixture
    def mock_preferences_repository(self, mocker):
        preferences_repo = mocker.AsyncMock(spec=PreferencesRepository)
        preferences_repo.get_preferences_by_user_id.return_value = Preferences(
            email_enabled=True,
            sms_enabled=False,
            property_types=["apartment", "house"],
            location="New York",
        )

        app.dependency_overrides[get_preferences_repository] = lambda: preferences_repo
        return preferences_repo

    @pytest.fixture
    def mock_user_repository(self, mocker):
        user_repo = mocker.AsyncMock(spec=UserRepository)
        user_repo.get_user_by_id.return_value = User(
            id="1",
            email="test@test",
            phone_number="1234567890",
        )
        app.dependency_overrides[get_user_repository] = lambda: user_repo
        return user_repo

    @pytest.fixture
    def test_client(self):
        """Provides a test client with mocked dependencies."""
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_get_preferences_positive(
        self, mock_preferences_repository, mock_user_repository, test_client
    ):
        """
        Light example of FastAPI integration testing
        """

        user_id = "2"
        # This is a demonstration of we can override the mock default values
        mock_user_repository.get_user_by_id.return_value = User(
            id=user_id,
            email="test@test",
            phone_number="1234567890",
        )

        response = test_client.get(f"/preferences/{user_id}")
        assert response.status_code == 200
        assert response.json() == {
            "user_id": user_id,
            "email_enabled": True,
            "sms_enabled": False,
            "property_types": ["apartment", "house"],
            "location": "New York",
        }

    @pytest.mark.asyncio
    async def test_get_preferences_negative(self, mock_user_repository, test_client):
        mock_user_repository.get_user_by_id.return_value = None
        user_id = "2"
        response = test_client.get(f"/preferences/{user_id}")
        assert response.status_code == 404
