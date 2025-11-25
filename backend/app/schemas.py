from pydantic import BaseModel
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import UUID
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


class CountryResponse(BaseModel):
    id: int
    code: str


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


# New schemas for account, publication, and user_account
class AccountResponse(BaseModel):
    id: UUID
    username: str
    followers: int


class PublicationResponse(BaseModel):
    id: UUID
    account_id: UUID
    type: str
    insights: Dict[str, Any]  # JSON data


class UserAccountResponse(BaseModel):
    id: UUID
    user_id: int
    account_id: UUID


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


class AccountCreate(BaseModel):
    username: str
    followers: int


class PublicationCreate(BaseModel):
    account_id: UUID
    type: str
    insights: Dict[str, Any]  # JSON data


class UserAccountCreate(BaseModel):
    user_id: int
    account_id: UUID


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


class AccountUpdate(BaseModel):
    username: Optional[str] = None
    followers: Optional[int] = None


class PublicationUpdate(BaseModel):
    account_id: Optional[UUID] = None
    type: Optional[str] = None
    insights: Optional[Dict[str, Any]] = None


class UserAccountUpdate(BaseModel):
    user_id: Optional[int] = None
    account_id: Optional[UUID] = None


# Input schemas for endpoints
class CampaignsQueryParams(BaseModel):
    organization_id: Optional[int] = None


class ApplicationsQueryParams(BaseModel):
    campaign_id: int