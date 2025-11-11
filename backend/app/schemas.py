from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from app.db.models import MediaType, ApplicationStatus

class DatabaseType(str, Enum):
    SCYLLA = "scylla"
    POSTGRES = "postgres"
    DUCKDB = "duckdb"

class CampaignRequirement(BaseModel):
    media_type: MediaType
    count: int

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
    requirements: List[CampaignRequirement] = []


class CampaignApplicationResponse(BaseModel):
    id: int
    campaign_id: int
    user_id: int
    status: ApplicationStatus


# Create schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class OrganizationCreate(BaseModel):
    name: str


class CampaignCreate(BaseModel):
    organizer_id: int
    name: str
    requirements: List[CampaignRequirement] = []


class CampaignApplicationCreate(BaseModel):
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
    requirements: Optional[List[CampaignRequirement]] = None


class CampaignApplicationUpdate(BaseModel):
    campaign_id: Optional[int] = None
    user_id: Optional[int] = None
    status: Optional[ApplicationStatus] = None


# Input schemas for endpoints
class CampaignsQueryParams(BaseModel):
    organization_id: Optional[int] = None


class ApplicationsQueryParams(BaseModel):
    campaign_id: int