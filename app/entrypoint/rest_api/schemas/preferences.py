from typing import Optional

from pydantic import BaseModel


class PreferencesResponse(BaseModel):
    user_id: str
    email_enabled: bool
    sms_enabled: bool
    property_types: list[str]
    location: Optional[str]


class PreferencesInput(BaseModel):
    email_enabled: bool = True
    sms_enabled: bool = False
    # COMMENT: It's safe to default to a mutable structure in a Pydantic model
    property_types: list[str] = []
    location: str = ""
