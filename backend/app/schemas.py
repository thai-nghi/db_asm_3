from pydantic import BaseModel
from enum import Enum
from typing import Optional
from app.db.models import MediaType, ApplicationStatus

class DatabaseType(str, Enum):
    SCYLLA = "scylla"
    POSTGRES = "postgres"
    DUCKDB = "duckdb"


# Update schemas
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None


class CampaignUpdate(BaseModel):
    organizer_id: Optional[int] = None
    name: Optional[str] = None


class CampaignRequirementsUpdate(BaseModel):
    campaign_id: Optional[int] = None
    media_type: Optional[MediaType] = None


class CampaignApplicationUpdate(BaseModel):
    campaign_id: Optional[int] = None
    user_id: Optional[int] = None
    status: Optional[ApplicationStatus] = None