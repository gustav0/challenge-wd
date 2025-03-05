from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas import Preferences
from app.infraestructure.db.models import Preferences as PreferencesTable
from app.ports.preferences_repository import PreferencesRepository

import logging

logger = logging.getLogger(__name__)

class DatabasePreferencesRepository(PreferencesRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_preferences_by_user_id(self, user_id: str) -> Optional[Preferences]:
        logger.info(f"DatabasePreferencesRepository/get_preferences_by_user_id: {user_id}")
        stmt = select(PreferencesTable).where(PreferencesTable.user_id == user_id)

        result = await self.session.execute(stmt)
        record = result.scalars().one_or_none()

        if not record:
            return None

        return Preferences.from_orm(record)

    async def upsert_preferences(self, user_id: str, preferences: Preferences) -> int:
        values = {
            "email_enabled": preferences.email_enabled,
            "sms_enabled": preferences.sms_enabled,
            "property_types": preferences.property_types,
            "location": preferences.location,
        }
        stmt = (
            insert(PreferencesTable)
            .values(user_id=user_id, **values)
            .on_conflict_do_update(
                index_elements=[PreferencesTable.user_id],
                set_=values,
            )
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
