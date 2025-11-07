from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from app.db.models import MediaType, ApplicationStatus

class DatabaseType(str, Enum):
    SCYLLA = "scylla"
    POSTGRES = "postgres"
    DUCKDB = "duckdb"


# Response schemas
class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class OrganizationResponse(BaseModel):
    id: int
    name: str


class CampaignResponse(BaseModel):
    id: int
    organizer_id: int
    name: str


class CampaignRequirementsResponse(BaseModel):
    id: int
    campaign_id: int
    media_type: MediaType


class CampaignApplicationResponse(BaseModel):
    id: int
    campaign_id: int
    user_id: int
    status: ApplicationStatus


# Create schemas
class UserCreate(BaseModel):
    id: int
    username: str
    email: str
    password: str


class OrganizationCreate(BaseModel):
    id: int
    name: str


class CampaignCreate(BaseModel):
    id: int
    organizer_id: int
    name: str


class CampaignRequirementsCreate(BaseModel):
    id: int
    campaign_id: int
    media_type: MediaType


class CampaignApplicationCreate(BaseModel):
    id: int
    campaign_id: int
    user_id: int
    status: ApplicationStatus


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


# Input schemas for endpoints
class CampaignsQueryParams(BaseModel):
    organization_id: Optional[int] = None


class ApplicationsQueryParams(BaseModel):
    campaign_id: int