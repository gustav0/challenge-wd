from app.domain.exceptions import (
    PreferencesNotFoundException,
    PropertyNotFoundException,
    UserNotFoundException,
)

test_get_notification_by_id_raises_exception = [
    {
        "id": "user_not_found",
        "mock": {
            "get_user_by_id": None,
            "get_property_by_id": 1,
            "get_preferences_by_user_id": 1,
        },
        "expected_exception": UserNotFoundException,
    },
    {
        "id": "property_not_found",
        "mock": {
            "get_user_by_id": 1,
            "get_property_by_id": None,
            "get_preferences_by_user_id": 1,
        },
        "expected_exception": PropertyNotFoundException,
    },
    {
        "id": "preferences_not_found",
        "mock": {
            "get_user_by_id": 1,
            "get_property_by_id": 1,
            "get_preferences_by_user_id": None,
        },
        "expected_exception": PreferencesNotFoundException,
    },
]
