"""
Simple setup script to insert some data into the database
Leverages the FastAPI lifespan
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infraestructure.db.database import Session
from app.infraestructure.db.models import Preferences as PreferencesTable

logger = logging.getLogger(__name__)


async def count_preferences(session: AsyncSession) -> int:
    stmt = select(func.count(PreferencesTable.id))
    result = await session.execute(stmt)
    count = result.scalar_one()
    return count


async def insert_preferences(session: AsyncSession):
    preferences = [
        {
            "user_id": "1",
            "email_enabled": True,
            "sms_enabled": True,
            "property_types": ["apartment", "house"],
            "location": "New York",
        },
        {
            "user_id": "2",
            "email_enabled": True,
            "sms_enabled": False,
            "property_types": ["apartment"],
            "location": "Seatle",
        },
        {
            "user_id": "3",
            "email_enabled": False,
            "sms_enabled": True,
            "property_types": ["house"],
            "location": "Miami",
        },
        {
            "user_id": "4",
            "email_enabled": False,
            "sms_enabled": False,
            "property_types": ["villa"],
            "location": "San Francisco",
        },
    ]
    stmt = insert(PreferencesTable).values(preferences)
    await session.execute(stmt)
    await session.commit()


async def seed_initial_db_data():
    async with Session() as session:
        if await count_preferences(session) == 0:
            await insert_preferences(session)
            logger.info("Initial data inserted")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_initial_db_data()
    yield
