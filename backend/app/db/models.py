from enum import Enum
from sqlmodel import Field, SQLModel, create_engine, Relationship


# Enums
class MediaType(str, Enum):
    photo = "photo"
    video = "video"


class ApplicationStatus(str, Enum):
    pending = "pending"
    accept = "accept"
    declined = "declined"

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    email: str
    password: str

    # Relationship to applications
    applications: list["CampaignApplication"] = Relationship(back_populates="user")


class Organization(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str

    # Relationship to campaigns organized by this organization
    campaigns: list["Campaign"] = Relationship(back_populates="organizer")


class Campaign(SQLModel, table=True):
    id: int = Field(primary_key=True)
    organizer_id: int = Field(foreign_key="organization.id")
    name: str

    # Relationships
    organizer: Organization = Relationship(back_populates="campaigns")
    requirements: list["CampaignRequirements"] = Relationship(back_populates="campaign")
    applications: list["CampaignApplication"] = Relationship(back_populates="campaign")


class CampaignRequirements(SQLModel, table=True):
    __tablename__ = "campaign_requirements"
    
    id: int = Field(primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id")
    media_type: MediaType

    # Relationship
    campaign: Campaign = Relationship(back_populates="requirements")


class CampaignApplication(SQLModel, table=True):
    __tablename__ = "campaign_application"
    
    id: int = Field(primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id")
    user_id: int = Field(foreign_key="user.id")
    status: ApplicationStatus

    # Relationships
    campaign: Campaign = Relationship(back_populates="applications")
    user: User = Relationship(back_populates="applications")