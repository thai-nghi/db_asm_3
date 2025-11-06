from app.schemas import DatabaseType, UserUpdate, OrganizationUpdate, CampaignUpdate, CampaignApplicationUpdate
from app.db.postgres import engine as postgres_engine
from app.db.duck import engine as duckdb_engine
from app.db import models
from sqlmodel import Session, select
from typing import Optional

class PostgresConnector:
    def __init__(self):
        pass

    def all_users(self):
        with Session(postgres_engine) as session:
            statement = select(models.User)
            results = session.exec(statement)
            return results

    def all_organizations(self):
        with Session(postgres_engine) as session:
            statement = select(models.Organization)
            results = session.exec(statement)
            return results

    def all_campaigns(self, organization_id: Optional[int] = None):
        with Session(postgres_engine) as session:
            if organization_id:
                statement = select(models.Campaign).where(models.Campaign.organizer_id == organization_id)
            else:
                statement = select(models.Campaign)
            results = session.exec(statement)
            return results

    def campaign_applications(self, campaign_id: int):
        with Session(postgres_engine) as session:
            statement = select(models.CampaignApplication).where(models.CampaignApplication.campaign_id == campaign_id)
            results = session.exec(statement)
            return results

    def update_user(self, user_id: int, user_data: UserUpdate):
        with Session(postgres_engine) as session:
            statement = select(models.User).where(models.User.id == user_id)
            user = session.exec(statement).first()
            if user:
                update_dict = user_data.model_dump(exclude_unset=True)
                for key, value in update_dict.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
            return None

    def update_organization(self, organization_id: int, organization_data: OrganizationUpdate):
        with Session(postgres_engine) as session:
            statement = select(models.Organization).where(models.Organization.id == organization_id)
            organization = session.exec(statement).first()
            if organization:
                update_dict = organization_data.model_dump(exclude_unset=True)
                for key, value in update_dict.items():
                    if hasattr(organization, key):
                        setattr(organization, key, value)
                session.add(organization)
                session.commit()
                session.refresh(organization)
                return organization
            return None

    def update_campaign(self, campaign_id: int, campaign_data: CampaignUpdate):
        with Session(postgres_engine) as session:
            statement = select(models.Campaign).where(models.Campaign.id == campaign_id)
            campaign = session.exec(statement).first()
            if campaign:
                update_dict = campaign_data.model_dump(exclude_unset=True)
                for key, value in update_dict.items():
                    if hasattr(campaign, key):
                        setattr(campaign, key, value)
                session.add(campaign)
                session.commit()
                session.refresh(campaign)
                return campaign
            return None

    def update_application(self, application_id: int, application_data: CampaignApplicationUpdate):
        with Session(postgres_engine) as session:
            statement = select(models.CampaignApplication).where(models.CampaignApplication.id == application_id)
            application = session.exec(statement).first()
            if application:
                update_dict = application_data.model_dump(exclude_unset=True)
                for key, value in update_dict.items():
                    if hasattr(application, key):
                        setattr(application, key, value)
                session.add(application)
                session.commit()
                session.refresh(application)
                return application
            return None
        
    

class Connector:
    def __init__(self):
        self.postgres_connector = PostgresConnector()

    def all_users(self, db_type: str):
        if db_type == "postgres":
            return self.postgres_connector.all_users()
        # Add other database types here
        return []

    def all_organizations(self, db_type: str):
        if db_type == "postgres":
            return self.postgres_connector.all_organizations()
        # Add other database types here
        return []

    def all_campaigns(self, db_type: str, organization_id: Optional[int] = None):
        if db_type == "postgres":
            return self.postgres_connector.all_campaigns(organization_id)
        # Add other database types here
        return []

    def campaign_applications(self, db_type: str, campaign_id: int):
        if db_type == "postgres":
            return self.postgres_connector.campaign_applications(campaign_id)
        # Add other database types here
        return []

    def update_user(self, db_type: str, user_id: int, user_data: UserUpdate):
        if db_type == "postgres":
            return self.postgres_connector.update_user(user_id, user_data)
        # Add other database types here
        return None

    def update_organization(self, db_type: str, organization_id: int, organization_data: OrganizationUpdate):
        if db_type == "postgres":
            return self.postgres_connector.update_organization(organization_id, organization_data)
        # Add other database types here
        return None

    def update_campaign(self, db_type: str, campaign_id: int, campaign_data: CampaignUpdate):
        if db_type == "postgres":
            return self.postgres_connector.update_campaign(campaign_id, campaign_data)
        # Add other database types here
        return None

    def update_application(self, db_type: str, application_id: int, application_data: CampaignApplicationUpdate):
        if db_type == "postgres":
            return self.postgres_connector.update_application(application_id, application_data)
        # Add other database types here
        return None

def get_db_connector() -> Connector:
    return Connector()