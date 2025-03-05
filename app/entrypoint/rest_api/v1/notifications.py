import logging

from fastapi import APIRouter, Depends, HTTPException

from app.domain.exceptions import (
    NotificationNotFoundException,
    PreferencesNotFoundException,
    UserNotFoundException,
)
from app.domain.services.notification_service import NotificationService
from app.entrypoint.rest_api.dependencies import get_notifications_service

from ..schemas import notification as schema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/notifications/{notification_id}",
    response_model=schema.NotificationResponse,
)
async def get_notification(
    notification_id: int,
    notifications_service: NotificationService = Depends(get_notifications_service),
):
    """Get notification by ID"""
    logger.info(
        "GET /notifications/{notification_id}",
        extra={"notification_id": notification_id},
    )
    try:
        result = await notifications_service.get_notification_by_id(notification_id)
    except NotificationNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    print("DATA", result.model_dump())
    return schema.NotificationResponse(**result.model_dump())


@router.post(
    "/notifications/schedule",
    response_model=schema.ScheduleNotificationResponse,
    status_code=200,
)
async def schedule_notification(
    input: schema.ScheduleNotificationInput,
    notifications_service: NotificationService = Depends(get_notifications_service),
):
    """Schedule notification"""

    logger.info(
        "GET /notifications/schedule - Scheduling notification",
        extra={
            "user_id": input.user_id,
            "notification_message": input.message,
            "property_id": input.property_id,
            "scheduled_time_utc": input.scheduled_time_utc.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        },
    )

    try:
        result = await notifications_service.schedule_notification(
            user_id=input.user_id,
            property_id=input.property_id,
            message=input.message,
            scheduled_time_utc=input.scheduled_time_utc,
        )
    except PreferencesNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    return schema.ScheduleNotificationResponse(notification_ids=result)
