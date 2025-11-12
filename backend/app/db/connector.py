from app import schemas
from app.db.postgres import engine as postgres_engine
from app.db.duck import engine as duckdb_engine
from app.db import models
from sqlmodel import Session, select
from typing import List, Union
from app.db.scylla import session as scylla_session


class SQLConnector:
    def __init__(self, engine):
        self.engine = engine

    def all_users(self) -> List[schemas.UserResponse]:
        with Session(self.engine) as session:
            statement = select(models.User).order_by(models.User.id)
            results = session.exec(statement)
            return [schemas.UserResponse.model_validate(user.model_dump()) for user in results]

    def all_organizations(self) -> List[schemas.OrganizationResponse]:
        with Session(self.engine) as session:
            statement = select(models.Organization).order_by(models.Organization.id)
            results = session.exec(statement)
            return [schemas.OrganizationResponse.model_validate(org.model_dump()) for org in results]

    def campaign_applications(self, campaign_id: int | None = None, user_id: int | None = None) -> List[schemas.CampaignApplicationResponse]:
        with Session(self.engine) as session:
            statement = select(models.CampaignApplication)
            
            if campaign_id is not None:
                statement = statement.where(models.CampaignApplication.campaign_id == campaign_id)

            if user_id is not None:
                statement = statement.where(models.CampaignApplication.user_id == user_id)

            statement = statement.order_by(models.CampaignApplication.id)
            results = session.exec(statement)
            return [schemas.CampaignApplicationResponse.model_validate(app.model_dump()) for app in results]

    def update_user(self, user_id: int, user_data: schemas.UserUpdate) -> schemas.UserResponse | None:
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
                return schemas.UserResponse.model_validate(user.model_dump())
            return None

    def update_organization(self, organization_id: int, organization_data: schemas.OrganizationUpdate) -> schemas.OrganizationResponse | None:
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
                return schemas.OrganizationResponse.model_validate(organization.model_dump())
            return None

    def update_application(self, application_id: int, application_data: schemas.CampaignApplicationUpdate) -> schemas.CampaignApplicationResponse | None:
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
                return schemas.CampaignApplicationResponse.model_validate(application.model_dump())
            return None

    def create_user(self, user_data: schemas.UserCreate) -> schemas.UserResponse:
        with Session(self.engine) as session:
            user = models.User(**user_data.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
            return schemas.UserResponse.model_validate(user.model_dump())

    def create_organization(self, organization_data: schemas.OrganizationCreate) -> schemas.OrganizationResponse:
        with Session(self.engine) as session:
            organization = models.Organization(**organization_data.model_dump())
            session.add(organization)
            session.commit()
            session.refresh(organization)
            return schemas.OrganizationResponse.model_validate(organization.model_dump())

    def create_campaign(self, campaign_data: schemas.CampaignCreate) -> schemas.CampaignResponse:
        with Session(self.engine) as session:
            # Create campaign
            campaign_dict = {"organizer_id": campaign_data.organizer_id, "name": campaign_data.name}
            campaign = models.Campaign(**campaign_dict)
            session.add(campaign)
            session.commit()
            session.refresh(campaign)
            
            for requirement in campaign_data.requirements:
                req = models.CampaignRequirements(campaign_id=campaign.id, media_type=requirement.media_type, count=requirement.count)
                session.add(req)

            session.commit()
            
            return schemas.CampaignResponse(
                id=campaign.id,
                organizer_id=campaign.organizer_id,
                name=campaign.name,
                requirements=campaign_data.requirements
            )

    def all_campaigns(self, organization_id: int = None) -> schemas.CampaignResponse | None:
        with Session(self.engine) as session:
            # Get campaign
            campaign_stmt = select(models.Campaign)
            
            if organization_id is not None:
                campaign_stmt = campaign_stmt.where(models.Campaign.organizer_id == organization_id)
            
            campaigns = session.exec(campaign_stmt)
            if not campaigns:
                return None
            
            return [schemas.CampaignResponse(
                **campaign.model_dump(exclude={'requirements'}),
                requirements=[schemas.CampaignRequirement(**req.model_dump()) for req in campaign.requirements]
            )for campaign in campaigns]
                
    def update_campaign(self, campaign_id: int, campaign_data: schemas.CampaignUpdate) -> schemas.CampaignResponse | None:
        with Session(self.engine) as session:
            # Update campaign basic info
            campaign_stmt = select(models.Campaign).where(models.Campaign.id == campaign_id)
            campaign = session.exec(campaign_stmt).first()
            if not campaign:
                return None
                
            # Update campaign fields
            update_dict = campaign_data.model_dump(exclude={'requirements'}, exclude_unset=True)
            for key, value in update_dict.items():
                if hasattr(campaign, key):
                    setattr(campaign, key, value)
            
            # Handle requirements if provided
            if campaign_data.requirements is not None:
                # Delete existing requirements
                existing_req_stmt = select(models.CampaignRequirements).where(models.CampaignRequirements.campaign_id == campaign_id)
                existing_requirements = session.exec(existing_req_stmt).all()
                for req in existing_requirements:
                    session.delete(req)
                    
                for requirement in campaign_data.requirements:
                    req = models.CampaignRequirements(campaign_id=campaign.id, media_type=requirement.media_type, count=requirement.count)
                    session.add(req)
            
            session.add(campaign)
            session.commit()
            session.refresh(campaign)
            
            # Get current requirements to return
            req_stmt = select(models.CampaignRequirements).where(models.CampaignRequirements.campaign_id == campaign_id)
            requirements = session.exec(req_stmt).all()
            
            return schemas.CampaignResponse(
                id=campaign.id,
                organizer_id=campaign.organizer_id,
                name=campaign.name,
                requirements=[schemas.CampaignRequirement(**req.model_dump()) for req in requirements]
            )

    def create_application(self, application_data: schemas.CampaignApplicationCreate) -> schemas.CampaignApplicationResponse:
        with Session(self.engine) as session:
            application = models.CampaignApplication(**application_data.model_dump())
            session.add(application)
            session.commit()
            session.refresh(application)
            return schemas.CampaignApplicationResponse.model_validate(application.model_dump())
        
    

class ScyllaConnector:
    def __init__(self, session):
        self.session = session
        
        # Prepare commonly used statements for better performance
        self.prepare_statements()
    
    def prepare_statements(self):
        """Prepare commonly used SQL statements"""
        # User queries
        self.select_user_by_id_stmt = self.session.prepare("SELECT * FROM user WHERE id = ?")
        self.insert_user_stmt = self.session.prepare("INSERT INTO user (id, username, email, password) VALUES (?, ?, ?, ?)")
        
        # Organization queries
        self.select_org_by_id_stmt = self.session.prepare("SELECT * FROM organization WHERE id = ?")
        self.insert_org_stmt = self.session.prepare("INSERT INTO organization (id, name) VALUES (?, ?)")
        
        # Campaign queries
        self.select_campaign_by_id_stmt = self.session.prepare("SELECT * FROM campaign WHERE id = ?")
        self.insert_campaign_stmt = self.session.prepare("INSERT INTO campaign (id, organizer_id, name) VALUES (?, ?, ?)")
        self.select_campaigns_by_organizer_stmt = self.session.prepare("SELECT * FROM campaigns_by_organizer WHERE organizer_id = ?")
        
        # Campaign requirements queries
        self.select_requirements_by_campaign_stmt = self.session.prepare("SELECT * FROM requirements_by_campaign WHERE campaign_id = ?")
        self.insert_requirement_stmt = self.session.prepare("INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (?, ?, ?, ?)")
        self.delete_requirement_by_id_stmt = self.session.prepare("DELETE FROM campaign_requirements WHERE id = ?")
        self.select_requirements_by_media_type_stmt = self.session.prepare("SELECT * FROM requirements_by_media_type WHERE media_type = ?")
        
        # Application queries
        self.select_app_by_id_stmt = self.session.prepare("SELECT * FROM campaign_application WHERE id = ?")
        self.insert_app_stmt = self.session.prepare("INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (?, ?, ?, ?)")
        self.select_apps_by_campaign_stmt = self.session.prepare("SELECT * FROM applications_by_campaign WHERE campaign_id = ?")
        self.select_apps_by_user_stmt = self.session.prepare("SELECT * FROM applications_by_user WHERE user_id = ?")
        # Note: Cannot create materialized views with both campaign_id and user_id due to ScyllaDB limitations
        # (can only include one non-primary key column in materialized view primary key)
        
        # Sequence queries
        self.select_user_sequence_stmt = self.session.prepare("SELECT user_sequence FROM sequence_id WHERE id = ?")
        self.update_user_sequence_stmt = self.session.prepare("UPDATE sequence_id SET user_sequence = ? WHERE id = ?")
        self.select_org_sequence_stmt = self.session.prepare("SELECT organization_sequence FROM sequence_id WHERE id = ?")
        self.update_org_sequence_stmt = self.session.prepare("UPDATE sequence_id SET organization_sequence = ? WHERE id = ?")
        self.select_campaign_sequence_stmt = self.session.prepare("SELECT campaign_sequence FROM sequence_id WHERE id = ?")
        self.update_campaign_sequence_stmt = self.session.prepare("UPDATE sequence_id SET campaign_sequence = ? WHERE id = ?")
        self.select_req_sequence_stmt = self.session.prepare("SELECT requirements_sequence FROM sequence_id WHERE id = ?")
        self.update_req_sequence_stmt = self.session.prepare("UPDATE sequence_id SET requirements_sequence = ? WHERE id = ?")
        self.select_app_sequence_stmt = self.session.prepare("SELECT application_sequence FROM sequence_id WHERE id = ?")
        self.update_app_sequence_stmt = self.session.prepare("UPDATE sequence_id SET application_sequence = ? WHERE id = ?")

    def all_users(self) -> List[schemas.UserResponse]:
        """Get all users from ScyllaDB"""
        query = "SELECT * FROM user"
        rows = self.session.execute(query)

        users = [schemas.UserResponse(username=row.username, email=row.email, id=row.id) for row in rows]

        users.sort(key=lambda u: u.id)
        return users

    def all_organizations(self) -> List[schemas.OrganizationResponse]:
        """Get all organizations from ScyllaDB"""
        query = "SELECT * FROM organization"
        rows = self.session.execute(query)
        
        organizations = [schemas.OrganizationResponse(id=row.id, name=row.name) for row in rows]
        
        organizations.sort(key=lambda o: o.id)
        return organizations

    def all_campaigns(self, organization_id: int | None = None) -> List[schemas.CampaignResponse]:
        """Get all campaigns with requirements, optionally filtered by organization_id"""
        if organization_id:
            # Use materialized view for efficient querying - ORDER BY allowed with partition key restriction
            rows = self.session.execute(self.select_campaigns_by_organizer_stmt, [organization_id])
        else:
            # No ORDER BY without partition key restriction
            query = "SELECT * FROM campaign"
            rows = self.session.execute(query)
        
        campaigns = []
        for row in rows:
            # Get requirements for this campaign
            req_rows = self.session.execute(self.select_requirements_by_campaign_stmt, [row.id])
            
            requirements = []
            for req_row in req_rows:
                requirements.append(schemas.CampaignRequirement(
                    media_type=req_row.media_type,
                    count=req_row.count
                ))
            
            campaign_response = schemas.CampaignResponse(
                id=row.id,
                organizer_id=row.organizer_id,
                name=row.name,
                requirements=requirements
            )
            campaigns.append(campaign_response)
        
        campaigns.sort(key=lambda c: c.id)
        return campaigns

    def campaign_applications(self, campaign_id: int | None = None, user_id: int | None = None) -> List[schemas.CampaignApplicationResponse]:
        """Get all applications with optional filtering by campaign_id and/or user_id"""
        
        # Build query with proper WHERE clause structure
        if campaign_id is not None and user_id is not None:
            # Filter by both campaign_id and user_id
            # Since we can't create a materialized view with both non-primary key columns,
            # we'll query by campaign_id using the materialized view, then filter by user_id in Python
            rows = self.session.execute(self.select_apps_by_campaign_stmt, [campaign_id])
            # Filter by user_id in application logic
            applications = []
            for row in rows:
                if row.user_id == user_id:
                    applications.append(schemas.CampaignApplicationResponse(
                        id=row.id,
                        campaign_id=row.campaign_id,
                        user_id=row.user_id,
                        status=row.status
                    ))
        elif campaign_id is not None:
            # Filter by campaign_id only - ORDER BY allowed with partition key in materialized view
            rows = self.session.execute(self.select_apps_by_campaign_stmt, [campaign_id])
            applications = [schemas.CampaignApplicationResponse(
                id=row.id,
                campaign_id=row.campaign_id,
                user_id=row.user_id,
                status=row.status
            ) for row in rows]
        elif user_id is not None:
            # Filter by user_id only - use applications_by_user materialized view
            rows = self.session.execute(self.select_apps_by_user_stmt, [user_id])
            applications = [schemas.CampaignApplicationResponse(
                id=row.id,
                campaign_id=row.campaign_id,
                user_id=row.user_id,
                status=row.status
            ) for row in rows]
        else:
            # No filters - query all applications from base table
            query = "SELECT * FROM campaign_application"
            rows = self.session.execute(query)
            applications = [schemas.CampaignApplicationResponse(
                id=row.id,
                campaign_id=row.campaign_id,
                user_id=row.user_id,
                status=row.status
            ) for row in rows]
            
        applications.sort(key=lambda a: a.id)
        return applications

    def update_user(self, user_id: int, user_data: schemas.UserUpdate) -> schemas.UserResponse | None:
        """Update a user in ScyllaDB"""
        update_dict = user_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in update_dict.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        
        query = f"UPDATE user SET {', '.join(set_clauses)} WHERE id = %s"
        values.append(user_id)
        
        self.session.execute(query, values)
        
        # Return updated user
        result_rows = list(self.session.execute(self.select_user_by_id_stmt, [user_id]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.UserResponse(id=row.id, username=row.username, email=row.email)

    def update_organization(self, organization_id: int, organization_data: schemas.OrganizationUpdate) -> schemas.OrganizationResponse | None:
        """Update an organization in ScyllaDB"""
        update_dict = organization_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in update_dict.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        
        query = f"UPDATE organization SET {', '.join(set_clauses)} WHERE id = %s"
        values.append(organization_id)
        
        self.session.execute(query, values)
        
        # Return updated organization
        result_rows = list(self.session.execute(self.select_org_by_id_stmt, [organization_id]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.OrganizationResponse(id=row.id, name=row.name)

    def update_campaign(self, campaign_id: int, campaign_data: schemas.CampaignUpdate) -> schemas.CampaignResponse | None:
        """Update a campaign in ScyllaDB"""
        update_dict = campaign_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in update_dict.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        
        query = f"UPDATE campaign SET {', '.join(set_clauses)} WHERE id = %s"
        values.append(campaign_id)
        
        self.session.execute(query, values)
        
        # Return updated campaign with requirements
        result_rows = list(self.session.execute(self.select_campaign_by_id_stmt, [campaign_id]))
        if not result_rows:
            return None
        row = result_rows[0]
        
        # Get requirements for this campaign
        req_rows = self.session.execute(self.select_requirements_by_campaign_stmt, [campaign_id])
        requirements = []
        for req_row in req_rows:
            requirements.append(schemas.CampaignRequirement(
                media_type=req_row.media_type,
                count=req_row.count
            ))
        
        return schemas.CampaignResponse(
            id=row.id,
            organizer_id=row.organizer_id,
            name=row.name,
            requirements=requirements
        )

    def update_application(self, application_id: int, application_data: schemas.CampaignApplicationUpdate) -> schemas.CampaignApplicationResponse | None:
        """Update a campaign application in ScyllaDB"""
        update_dict = application_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        if 'status' in update_dict:
            update_dict['status'] = update_dict['status'].value

        set_clauses = []
        values = []
        for key, value in update_dict.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        
        query = f"UPDATE campaign_application SET {', '.join(set_clauses)} WHERE id = %s"
        values.append(application_id)

        self.session.execute(query, values)
        
        # Return updated application
        result_rows = list(self.session.execute(self.select_app_by_id_stmt, [application_id]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.CampaignApplicationResponse(
            id=row.id,
            campaign_id=row.campaign_id,
            user_id=row.user_id,
            status=row.status
        )

    def create_user(self, user_data: schemas.UserCreate) -> schemas.UserResponse | None:
        """Create a user in ScyllaDB"""

        # Fetch current user id
        current_id_result = list(self.session.execute(self.select_user_sequence_stmt, [0]))
        if not current_id_result:
            raise ValueError("Failed to retrieve current user ID")
        current_id = current_id_result[0]
        new_user_id = current_id[0] + 1

        data = user_data.model_dump()
        self.session.execute(self.insert_user_stmt, [new_user_id, data['username'], data['email'], data['password']])
        
        # Update saved id to new value
        self.session.execute(self.update_user_sequence_stmt, [new_user_id, 0])
        
        # Return created user
        result_rows = list(self.session.execute(self.select_user_by_id_stmt, [new_user_id]))
        if not result_rows:
            return None
        row = result_rows[0]

        return schemas.UserResponse(id=row.id, username=row.username, email=row.email)

    def create_organization(self, organization_data: schemas.OrganizationCreate) -> schemas.OrganizationResponse | None:
        """Create an organization in ScyllaDB"""
        
        # Fetch current organization id
        current_id_result = list(self.session.execute(self.select_org_sequence_stmt, [0]))
        if not current_id_result:
            raise ValueError("Failed to retrieve current organization ID")
        current_id = current_id_result[0]
        new_org_id = current_id[0] + 1
        
        data = organization_data.model_dump()
        self.session.execute(self.insert_org_stmt, [new_org_id, data['name']])
        
        # Update saved id to new value
        self.session.execute(self.update_org_sequence_stmt, [new_org_id, 0])
        
        # Return created organization
        result_rows = list(self.session.execute(self.select_org_by_id_stmt, [new_org_id]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.OrganizationResponse(id=row.id, name=row.name)

    def create_campaign(self, campaign_data: schemas.CampaignCreate) -> schemas.CampaignResponse | None:
        """Create a campaign with requirements in ScyllaDB"""
        
        # Fetch current campaign id
        current_id_result = list(self.session.execute(self.select_campaign_sequence_stmt, [0]))
        if not current_id_result:
            raise ValueError("Failed to retrieve current campaign ID")
        current_id = current_id_result[0]
        new_campaign_id = current_id[0] + 1
        
        # Create campaign
        self.session.execute(self.insert_campaign_stmt, [new_campaign_id, campaign_data.organizer_id, campaign_data.name])
        
        # Update campaign sequence
        self.session.execute(self.update_campaign_sequence_stmt, [new_campaign_id, 0])
        
        # Create requirements
        requirements_list = []
        for requirement in campaign_data.requirements:
            # Fetch current requirements id
            req_current_id_result = list(self.session.execute(self.select_req_sequence_stmt, [0]))
            if not req_current_id_result:
                raise ValueError("Failed to retrieve current requirements ID")
            req_current_id = req_current_id_result[0]
            new_req_id = req_current_id[0] + 1
            
            self.session.execute(self.insert_requirement_stmt, [new_req_id, new_campaign_id, requirement.media_type.value, requirement.count])
            
            # Update requirements sequence
            self.session.execute(self.update_req_sequence_stmt, [new_req_id, 0])
            
            requirements_list.append(requirement)
        
        return schemas.CampaignResponse(
            id=new_campaign_id,
            organizer_id=campaign_data.organizer_id,
            name=campaign_data.name,
            requirements=requirements_list
        )

    def update_campaign(self, campaign_id: int, campaign_data: schemas.CampaignUpdate) -> schemas.CampaignResponse | None:
        """Update campaign with requirements in ScyllaDB"""
        import time
        
        # Update campaign basic info
        update_dict = campaign_data.model_dump(exclude={'requirements'}, exclude_unset=True)
        if update_dict:
            set_clauses = []
            values = []
            for key, value in update_dict.items():
                set_clauses.append(f"{key} = %s")
                values.append(value)
            
            query = f"UPDATE campaign SET {', '.join(set_clauses)} WHERE id = %s"
            values.append(campaign_id)
            self.session.execute(query, values)
        
        # Handle requirements if provided
        if campaign_data.requirements is not None:
            # Delete existing requirements
            existing_req_rows = self.session.execute(self.select_requirements_by_campaign_stmt, [campaign_id])
            
            for row in existing_req_rows:
                self.session.execute(self.delete_requirement_by_id_stmt, [row.id])
            
            # Create new requirements
            for idx, requirement in enumerate(campaign_data.requirements):
                current_id_result = list(self.session.execute(self.select_req_sequence_stmt, [0]))
                if not current_id_result:
                    raise ValueError("Failed to retrieve current requirements ID")
                req_id = current_id_result[0][0] + 1
                self.session.execute(self.insert_requirement_stmt, [req_id, campaign_id, requirement.media_type.value, requirement.count])
                self.session.execute(self.update_req_sequence_stmt, [req_id, 0])
        
        # Return updated campaign with requirements
        campaign_result = list(self.session.execute(self.select_campaign_by_id_stmt, [campaign_id]))
        if not campaign_result:
            return None
        campaign_row = campaign_result[0]
            
        # Get requirements
        req_rows = self.session.execute(self.select_requirements_by_campaign_stmt, [campaign_id])
        
        requirements = []
        for req_row in req_rows:
            requirements.append(schemas.CampaignRequirement(
                media_type=req_row.media_type,
                count=req_row.count
            ))
        
        return schemas.CampaignResponse(
            id=campaign_row.id,
            organizer_id=campaign_row.organizer_id,
            name=campaign_row.name,
            requirements=requirements
        )

    def create_application(self, application_data: schemas.CampaignApplicationCreate) -> schemas.CampaignApplicationResponse | None:
        """Create a campaign application in ScyllaDB"""
        
        # Fetch current application id
        current_id_result = list(self.session.execute(self.select_app_sequence_stmt, [0]))
        if not current_id_result:
            raise ValueError("Failed to retrieve current application ID")
        current_id = current_id_result[0]
        new_app_id = current_id[0] + 1
        
        data = application_data.model_dump()
        self.session.execute(self.insert_app_stmt, [new_app_id, data['campaign_id'], data['user_id'], data['status']])
        
        # Update saved id to new value
        self.session.execute(self.update_app_sequence_stmt, [new_app_id, 0])
        
        # Return created application
        result_rows = list(self.session.execute(self.select_app_by_id_stmt, [new_app_id]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.CampaignApplicationResponse(
            id=row.id,
            campaign_id=row.campaign_id,
            user_id=row.user_id,
            status=row.status
        )


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

    def all_campaigns(self, db_type: str, organization_id: int | None = None) -> List[schemas.CampaignResponse]:
        if db_type == "postgres":
            return self.postgres_connector.all_campaigns(organization_id)
        if db_type == "duckdb":
            return self.duck_connector.all_campaigns(organization_id)
        if db_type == "scylla":
            return self.scylla_connector.all_campaigns(organization_id)
        return []

    def campaign_applications(self, db_type: str, campaign_id: int | None = None, user_id: int | None = None) -> List[schemas.CampaignApplicationResponse]:
        if db_type == "postgres":
            return self.postgres_connector.campaign_applications(campaign_id, user_id)
        if db_type == "duckdb":
            return self.duck_connector.campaign_applications(campaign_id, user_id)
        if db_type == "scylla":
            return self.scylla_connector.campaign_applications(campaign_id, user_id)
        return []

    def update_user(self, db_type: str, user_id: int, user_data: schemas.UserUpdate) -> schemas.UserResponse | None:
        if db_type == "postgres":
            return self.postgres_connector.update_user(user_id, user_data)
        if db_type == "duckdb":
            return self.duck_connector.update_user(user_id, user_data)
        if db_type == "scylla":
            return self.scylla_connector.update_user(user_id, user_data)
        return None

    def update_organization(self, db_type: str, organization_id: int, organization_data: schemas.OrganizationUpdate) -> schemas.OrganizationResponse | None:
        if db_type == "postgres":
            return self.postgres_connector.update_organization(organization_id, organization_data)
        if db_type == "duckdb":
            return self.duck_connector.update_organization(organization_id, organization_data)
        if db_type == "scylla":
            return self.scylla_connector.update_organization(organization_id, organization_data)
        return None

    def update_campaign(self, db_type: str, campaign_id: int, campaign_data: schemas.CampaignUpdate) -> schemas.CampaignResponse | None:
        if db_type == "postgres":
            return self.postgres_connector.update_campaign(campaign_id, campaign_data)
        if db_type == "duckdb":
            return self.duck_connector.update_campaign(campaign_id, campaign_data)
        if db_type == "scylla":
            return self.scylla_connector.update_campaign(campaign_id, campaign_data)
        return None

    def update_application(self, db_type: str, application_id: int, application_data: schemas.CampaignApplicationUpdate) -> schemas.CampaignApplicationResponse | None:
        if db_type == "postgres":
            return self.postgres_connector.update_application(application_id, application_data)
        if db_type == "duckdb":
            return self.duck_connector.update_application(application_id, application_data)
        if db_type == "scylla":
            return self.scylla_connector.update_application(application_id, application_data)
        return None

    def create_user(self, db_type: str, user_data: schemas.UserCreate) -> schemas.UserResponse | None:
        if db_type == "postgres":
            return self.postgres_connector.create_user(user_data)
        if db_type == "duckdb":
            return self.duck_connector.create_user(user_data)
        if db_type == "scylla":
            return self.scylla_connector.create_user(user_data)
        return None

    def create_organization(self, db_type: str, organization_data: schemas.OrganizationCreate) -> schemas.OrganizationResponse | None:
        if db_type == "postgres":
            return self.postgres_connector.create_organization(organization_data)
        if db_type == "duckdb":
            return self.duck_connector.create_organization(organization_data)
        if db_type == "scylla":
            return self.scylla_connector.create_organization(organization_data)
        return None

    def create_campaign(self, db_type: str, campaign_data: schemas.CampaignCreate) -> schemas.CampaignResponse | None:
        if db_type == "postgres":
            return self.postgres_connector.create_campaign(campaign_data)
        if db_type == "duckdb":
            return self.duck_connector.create_campaign(campaign_data)
        if db_type == "scylla":
            return self.scylla_connector.create_campaign(campaign_data)
        return None

    def create_application(self, db_type: str, application_data: schemas.CampaignApplicationCreate) -> schemas.CampaignApplicationResponse | None:
        if db_type == "postgres":
            return self.postgres_connector.create_application(application_data)
        if db_type == "duckdb":
            return self.duck_connector.create_application(application_data)
        if db_type == "scylla":
            return self.scylla_connector.create_application(application_data)
        return None

def get_db_connector() -> Connector:
    return Connector()