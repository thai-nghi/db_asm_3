from app import schemas
from app.db.postgres import engine as postgres_engine
from app.db.duck import engine as duckdb_engine
from app.db import models
from sqlmodel import Session, select
from typing import Optional, List, Union
from app.db.scylla import session as scylla_session


class SQLConnector:
    def __init__(self, engine):
        self.engine = engine

    def all_users(self) -> List[schemas.UserResponse]:
        with Session(self.engine) as session:
            statement = select(models.User)
            results = session.exec(statement)
            return [schemas.UserResponse.model_validate(user) for user in results]

    def all_organizations(self) -> List[schemas.OrganizationResponse]:
        with Session(self.engine) as session:
            statement = select(models.Organization)
            results = session.exec(statement)
            return [schemas.OrganizationResponse.model_validate(org) for org in results]

    def all_campaigns(self, organization_id: Optional[int] = None) -> List[schemas.CampaignResponse]:
        with Session(self.engine) as session:
            if organization_id:
                statement = select(models.Campaign).where(models.Campaign.organizer_id == organization_id)
            else:
                statement = select(models.Campaign)
            results = session.exec(statement)
            return [schemas.CampaignResponse.model_validate(campaign) for campaign in results]

    def campaign_applications(self, campaign_id: int) -> List[schemas.CampaignApplicationResponse]:
        with Session(self.engine) as session:
            statement = select(models.CampaignApplication).where(models.CampaignApplication.campaign_id == campaign_id)
            results = session.exec(statement)
            return [schemas.CampaignApplicationResponse.model_validate(app) for app in results]

    def update_user(self, user_id: int, user_data: schemas.UserUpdate) -> Optional[schemas.UserResponse]:
        with Session(self.engine) as session:
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
                return schemas.UserResponse.model_validate(user)
            return None

    def update_organization(self, organization_id: int, organization_data: schemas.OrganizationUpdate) -> Optional[schemas.OrganizationResponse]:
        with Session(self.engine) as session:
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
                return schemas.OrganizationResponse.model_validate(organization)
            return None

    def update_campaign(self, campaign_id: int, campaign_data: schemas.CampaignUpdate) -> Optional[schemas.CampaignResponse]:
        with Session(self.engine) as session:
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
                return schemas.CampaignResponse.model_validate(campaign)
            return None

    def update_application(self, application_id: int, application_data: schemas.CampaignApplicationUpdate) -> Optional[schemas.CampaignApplicationResponse]:
        with Session(self.engine) as session:
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
                return schemas.CampaignApplicationResponse.model_validate(application)
            return None

    def create_user(self, user_data: schemas.UserCreate) -> schemas.UserResponse:
        with Session(self.engine) as session:
            user = models.User(**user_data.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
            return schemas.UserResponse.model_validate(user)

    def create_organization(self, organization_data: schemas.OrganizationCreate) -> schemas.OrganizationResponse:
        with Session(self.engine) as session:
            organization = models.Organization(**organization_data.model_dump())
            session.add(organization)
            session.commit()
            session.refresh(organization)
            return schemas.OrganizationResponse.model_validate(organization)

    def create_campaign(self, campaign_data: schemas.CampaignCreate) -> schemas.CampaignResponse:
        with Session(self.engine) as session:
            campaign = models.Campaign(**campaign_data.model_dump())
            session.add(campaign)
            session.commit()
            session.refresh(campaign)
            return schemas.CampaignResponse.model_validate(campaign)

    def create_campaign_requirements(self, requirements_data: schemas.CampaignRequirementsCreate) -> schemas.CampaignRequirementsResponse:
        with Session(self.engine) as session:
            requirements = models.CampaignRequirements(**requirements_data.model_dump())
            session.add(requirements)
            session.commit()
            session.refresh(requirements)
            return schemas.CampaignRequirementsResponse.model_validate(requirements)

    def create_application(self, application_data: schemas.CampaignApplicationCreate) -> schemas.CampaignApplicationResponse:
        with Session(self.engine) as session:
            application = models.CampaignApplication(**application_data.model_dump())
            session.add(application)
            session.commit()
            session.refresh(application)
            return schemas.CampaignApplicationResponse.model_validate(application)
        
    

class ScyllaConnector:
    def __init__(self, session):
        self.session = session

    def all_users(self) -> List[schemas.UserResponse]:
        """Get all users from ScyllaDB"""
        query = "SELECT * FROM user"
        rows = self.session.execute(query)
        return [schemas.UserResponse.model_validate(dict(row)) for row in rows]

    def all_organizations(self) -> List[schemas.OrganizationResponse]:
        """Get all organizations from ScyllaDB"""
        query = "SELECT * FROM organization"
        rows = self.session.execute(query)
        return [schemas.OrganizationResponse.model_validate(dict(row)) for row in rows]

    def all_campaigns(self, organization_id: Optional[int] = None) -> List[schemas.CampaignResponse]:
        """Get all campaigns, optionally filtered by organization_id"""
        if organization_id:
            # Use materialized view for efficient querying
            query = "SELECT * FROM campaigns_by_organizer WHERE organizer_id = ?"
            rows = self.session.execute(query, [organization_id])
        else:
            query = "SELECT * FROM campaign"
            rows = self.session.execute(query)
        return [schemas.CampaignResponse.model_validate(dict(row)) for row in rows]

    def campaign_applications(self, campaign_id: int) -> List[schemas.CampaignApplicationResponse]:
        """Get all applications for a specific campaign"""
        # Use materialized view for efficient querying
        query = "SELECT * FROM applications_by_campaign WHERE campaign_id = ?"
        rows = self.session.execute(query, [campaign_id])
        return [schemas.CampaignApplicationResponse.model_validate(dict(row)) for row in rows]

    def update_user(self, user_id: int, user_data: schemas.UserUpdate) -> Optional[schemas.UserResponse]:
        """Update a user in ScyllaDB"""
        update_dict = user_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in update_dict.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        query = f"UPDATE user SET {', '.join(set_clauses)} WHERE id = ?"
        values.append(user_id)
        
        self.session.execute(query, values)
        
        # Return updated user
        select_query = "SELECT * FROM user WHERE id = ?"
        row = self.session.execute(select_query, [user_id]).one_or_none()
        return schemas.UserResponse.model_validate(dict(row)) if row else None

    def update_organization(self, organization_id: int, organization_data: schemas.OrganizationUpdate) -> Optional[schemas.OrganizationResponse]:
        """Update an organization in ScyllaDB"""
        update_dict = organization_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in update_dict.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        query = f"UPDATE organization SET {', '.join(set_clauses)} WHERE id = ?"
        values.append(organization_id)
        
        self.session.execute(query, values)
        
        # Return updated organization
        select_query = "SELECT * FROM organization WHERE id = ?"
        row = self.session.execute(select_query, [organization_id]).one_or_none()
        return schemas.OrganizationResponse.model_validate(dict(row)) if row else None

    def update_campaign(self, campaign_id: int, campaign_data: schemas.CampaignUpdate) -> Optional[schemas.CampaignResponse]:
        """Update a campaign in ScyllaDB"""
        update_dict = campaign_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in update_dict.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        query = f"UPDATE campaign SET {', '.join(set_clauses)} WHERE id = ?"
        values.append(campaign_id)
        
        self.session.execute(query, values)
        
        # Return updated campaign
        select_query = "SELECT * FROM campaign WHERE id = ?"
        row = self.session.execute(select_query, [campaign_id]).one_or_none()
        return schemas.CampaignResponse.model_validate(dict(row)) if row else None

    def update_application(self, application_id: int, application_data: schemas.CampaignApplicationUpdate) -> Optional[schemas.CampaignApplicationResponse]:
        """Update a campaign application in ScyllaDB"""
        update_dict = application_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in update_dict.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        query = f"UPDATE campaign_application SET {', '.join(set_clauses)} WHERE id = ?"
        values.append(application_id)
        
        self.session.execute(query, values)
        
        # Return updated application
        select_query = "SELECT * FROM campaign_application WHERE id = ?"
        row = self.session.execute(select_query, [application_id]).one_or_none()
        return schemas.CampaignApplicationResponse.model_validate(dict(row)) if row else None

    def create_user(self, user_data: schemas.UserCreate) -> Optional[schemas.UserResponse]:
        """Create a user in ScyllaDB"""
        data = user_data.model_dump()
        query = "INSERT INTO user (id, username, email, password) VALUES (?, ?, ?, ?)"
        values = [data['id'], data['username'], data['email'], data['password']]
        self.session.execute(query, values)
        
        # Return created user
        select_query = "SELECT * FROM user WHERE id = ?"
        row = self.session.execute(select_query, [data['id']]).one_or_none()
        return schemas.UserResponse.model_validate(dict(row)) if row else None

    def create_organization(self, organization_data: schemas.OrganizationCreate) -> Optional[schemas.OrganizationResponse]:
        """Create an organization in ScyllaDB"""
        data = organization_data.model_dump()
        query = "INSERT INTO organization (id, name) VALUES (?, ?)"
        values = [data['id'], data['name']]
        self.session.execute(query, values)
        
        # Return created organization
        select_query = "SELECT * FROM organization WHERE id = ?"
        row = self.session.execute(select_query, [data['id']]).one_or_none()
        return schemas.OrganizationResponse.model_validate(dict(row)) if row else None

    def create_campaign(self, campaign_data: schemas.CampaignCreate) -> Optional[schemas.CampaignResponse]:
        """Create a campaign in ScyllaDB"""
        data = campaign_data.model_dump()
        query = "INSERT INTO campaign (id, organizer_id, name) VALUES (?, ?, ?)"
        values = [data['id'], data['organizer_id'], data['name']]
        self.session.execute(query, values)
        
        # Return created campaign
        select_query = "SELECT * FROM campaign WHERE id = ?"
        row = self.session.execute(select_query, [data['id']]).one_or_none()
        return schemas.CampaignResponse.model_validate(dict(row)) if row else None

    def create_campaign_requirements(self, requirements_data: schemas.CampaignRequirementsCreate) -> Optional[schemas.CampaignRequirementsResponse]:
        """Create campaign requirements in ScyllaDB"""
        data = requirements_data.model_dump()
        query = "INSERT INTO campaign_requirements (id, campaign_id, media_type) VALUES (?, ?, ?)"
        values = [data['id'], data['campaign_id'], data['media_type']]
        self.session.execute(query, values)
        
        # Return created requirements
        select_query = "SELECT * FROM campaign_requirements WHERE id = ?"
        row = self.session.execute(select_query, [data['id']]).one_or_none()
        return schemas.CampaignRequirementsResponse.model_validate(dict(row)) if row else None

    def create_application(self, application_data: schemas.CampaignApplicationCreate) -> Optional[schemas.CampaignApplicationResponse]:
        """Create a campaign application in ScyllaDB"""
        data = application_data.model_dump()
        query = "INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (?, ?, ?, ?)"
        values = [data['id'], data['campaign_id'], data['user_id'], data['status']]
        self.session.execute(query, values)
        
        # Return created application
        select_query = "SELECT * FROM campaign_application WHERE id = ?"
        row = self.session.execute(select_query, [data['id']]).one_or_none()
        return schemas.CampaignApplicationResponse.model_validate(dict(row)) if row else None


class Connector:
    def __init__(self):
        self.postgres_connector = SQLConnector(postgres_engine)
        self.duck_connector = SQLConnector(duckdb_engine)
        self.scylla_connector = ScyllaConnector(scylla_session)

    def all_users(self, db_type: str) -> List[schemas.UserResponse]:
        if db_type == "postgres":
            return self.postgres_connector.all_users()
        if db_type == "duckdb":
            return self.duck_connector.all_users()
        if db_type == "scylla":
            return self.scylla_connector.all_users()
        return []

    def all_organizations(self, db_type: str) -> List[schemas.OrganizationResponse]:
        if db_type == "postgres":
            return self.postgres_connector.all_organizations()
        if db_type == "duckdb":
            return self.duck_connector.all_organizations()
        if db_type == "scylla":
            return self.scylla_connector.all_organizations()
        return []

    def all_campaigns(self, db_type: str, organization_id: Optional[int] = None) -> List[schemas.CampaignResponse]:
        if db_type == "postgres":
            return self.postgres_connector.all_campaigns(organization_id)
        if db_type == "duckdb":
            return self.duck_connector.all_campaigns(organization_id)
        if db_type == "scylla":
            return self.scylla_connector.all_campaigns(organization_id)
        return []

    def campaign_applications(self, db_type: str, campaign_id: int) -> List[schemas.CampaignApplicationResponse]:
        if db_type == "postgres":
            return self.postgres_connector.campaign_applications(campaign_id)
        if db_type == "duckdb":
            return self.duck_connector.campaign_applications(campaign_id)
        if db_type == "scylla":
            return self.scylla_connector.campaign_applications(campaign_id)
        return []

    def update_user(self, db_type: str, user_id: int, user_data: schemas.UserUpdate) -> Optional[schemas.UserResponse]:
        if db_type == "postgres":
            return self.postgres_connector.update_user(user_id, user_data)
        if db_type == "duckdb":
            return self.duck_connector.update_user(user_id, user_data)
        if db_type == "scylla":
            return self.scylla_connector.update_user(user_id, user_data)
        return None

    def update_organization(self, db_type: str, organization_id: int, organization_data: schemas.OrganizationUpdate) -> Optional[schemas.OrganizationResponse]:
        if db_type == "postgres":
            return self.postgres_connector.update_organization(organization_id, organization_data)
        if db_type == "duckdb":
            return self.duck_connector.update_organization(organization_id, organization_data)
        if db_type == "scylla":
            return self.scylla_connector.update_organization(organization_id, organization_data)
        return None

    def update_campaign(self, db_type: str, campaign_id: int, campaign_data: schemas.CampaignUpdate) -> Optional[schemas.CampaignResponse]:
        if db_type == "postgres":
            return self.postgres_connector.update_campaign(campaign_id, campaign_data)
        if db_type == "duckdb":
            return self.duck_connector.update_campaign(campaign_id, campaign_data)
        if db_type == "scylla":
            return self.scylla_connector.update_campaign(campaign_id, campaign_data)
        return None

    def update_application(self, db_type: str, application_id: int, application_data: schemas.CampaignApplicationUpdate) -> Optional[schemas.CampaignApplicationResponse]:
        if db_type == "postgres":
            return self.postgres_connector.update_application(application_id, application_data)
        if db_type == "duckdb":
            return self.duck_connector.update_application(application_id, application_data)
        if db_type == "scylla":
            return self.scylla_connector.update_application(application_id, application_data)
        return None

    def create_user(self, db_type: str, user_data: schemas.UserCreate) -> Optional[schemas.UserResponse]:
        if db_type == "postgres":
            return self.postgres_connector.create_user(user_data)
        if db_type == "duckdb":
            return self.duck_connector.create_user(user_data)
        if db_type == "scylla":
            return self.scylla_connector.create_user(user_data)
        return None

    def create_organization(self, db_type: str, organization_data: schemas.OrganizationCreate) -> Optional[schemas.OrganizationResponse]:
        if db_type == "postgres":
            return self.postgres_connector.create_organization(organization_data)
        if db_type == "duckdb":
            return self.duck_connector.create_organization(organization_data)
        if db_type == "scylla":
            return self.scylla_connector.create_organization(organization_data)
        return None

    def create_campaign(self, db_type: str, campaign_data: schemas.CampaignCreate) -> Optional[schemas.CampaignResponse]:
        if db_type == "postgres":
            return self.postgres_connector.create_campaign(campaign_data)
        if db_type == "duckdb":
            return self.duck_connector.create_campaign(campaign_data)
        if db_type == "scylla":
            return self.scylla_connector.create_campaign(campaign_data)
        return None

    def create_campaign_requirements(self, db_type: str, requirements_data: schemas.CampaignRequirementsCreate) -> Optional[schemas.CampaignRequirementsResponse]:
        if db_type == "postgres":
            return self.postgres_connector.create_campaign_requirements(requirements_data)
        if db_type == "duckdb":
            return self.duck_connector.create_campaign_requirements(requirements_data)
        if db_type == "scylla":
            return self.scylla_connector.create_campaign_requirements(requirements_data)
        return None

    def create_application(self, db_type: str, application_data: schemas.CampaignApplicationCreate) -> Optional[schemas.CampaignApplicationResponse]:
        if db_type == "postgres":
            return self.postgres_connector.create_application(application_data)
        if db_type == "duckdb":
            return self.duck_connector.create_application(application_data)
        if db_type == "scylla":
            return self.scylla_connector.create_application(application_data)
        return None

def get_db_connector() -> Connector:
    return Connector()