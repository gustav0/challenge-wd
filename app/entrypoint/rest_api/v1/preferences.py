import logging

from fastapi import APIRouter, Depends, HTTPException

from app.domain.exceptions import PreferencesNotFoundException, UserNotFoundException
from app.domain.schemas import Preferences
from app.domain.services.preferences_service import PreferencesService
from app.entrypoint.rest_api.dependencies import get_preferences_service

from ..schemas import preferences as schema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.put(
    # We could also support PATCH
    "/preferences/{user_id}",
    response_model=schema.PreferencesResponse,
)
async def update_user_preferences(
    user_id: str,
    preferences: schema.PreferencesInput,
    preferences_service: PreferencesService = Depends(get_preferences_service),
):
    """Update user preferences"""
    try:
        result = await preferences_service.update_user_preferences(
            user_id,
            Preferences(**preferences.model_dump()),
        )
    except UserNotFoundException as e:
        # Even if we know the reason for the error, we might not want to expose it
        raise HTTPException(status_code=404, detail=str(e))
    except PreferencesNotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=404, detail=f"Could not fetch preferences for user {user_id}"
        )

    return schema.PreferencesResponse(user_id=user_id, **result.model_dump())


@router.get("/preferences/{user_id}", response_model=schema.PreferencesResponse)
async def get_user_preferences(
    user_id: str,
    preferences_service: PreferencesService = Depends(get_preferences_service),
):
    """Fetch user preferences by user ID"""
    # This layer should map domain errors to HTTP errors (as this is a REST API).
    # Or we could have a separate layer for mapping domain errors to HTTP errors,
    # like a middleware
    try:
        result = await preferences_service.get_preferences(user_id)
    except UserNotFoundException as e:
        # Even if we know the reason for the error, we might not want to expose it
        raise HTTPException(status_code=404, detail=str(e))
    except PreferencesNotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=404, detail=f"Could not fetch preferences for user {user_id}"
        )

    return schema.PreferencesResponse(user_id=user_id, **result.model_dump())
