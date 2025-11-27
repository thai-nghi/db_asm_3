from app import schemas
from app.db.postgres import engine as postgres_engine
from app.db import models
from sqlmodel import Session, select
from typing import List
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

    def all_countries(self) -> List[schemas.CountryResponse]:
        with Session(self.engine) as session:
            statement = select(models.Country).order_by(models.Country.id)
            results = session.exec(statement)
            return [schemas.CountryResponse.model_validate(country.model_dump()) for country in results]

    def all_applications(self, campaign_id: int | None = None, user_id: int | None = None) -> List[schemas.CampaignApplicationResponse]:
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

    def create_user(self, id: int, user_data: schemas.UserCreate) -> schemas.UserResponse:
        with Session(self.engine) as session:
            user = models.User(id=id, **user_data.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
            return schemas.UserResponse.model_validate(user.model_dump())

    def create_organization(self, id: int, organization_data: schemas.OrganizationCreate) -> schemas.OrganizationResponse:
        with Session(self.engine) as session:
            organization = models.Organization(id=id, **organization_data.model_dump())
            session.add(organization)
            session.commit()
            session.refresh(organization)
            return schemas.OrganizationResponse.model_validate(organization.model_dump())

    def create_campaign(self, id: int, campaign_data: schemas.CampaignCreate) -> schemas.CampaignResponse:
        with Session(self.engine) as session:
            # Create campaign
            campaign_dict = {"organizer_id": campaign_data.organizer_id, "name": campaign_data.name}
            campaign = models.Campaign(id=id, **campaign_dict)
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

    def create_application(self, id: int, application_data: schemas.CampaignApplicationCreate) -> schemas.CampaignApplicationResponse:
        with Session(self.engine) as session:
            application = models.CampaignApplication(id=id, **application_data.model_dump())
            session.add(application)
            session.commit()
            session.refresh(application)
            return schemas.CampaignApplicationResponse.model_validate(application.model_dump())
        
    def get_user_country(self, user_id: int) -> schemas.CountryResponse:
        with Session(self.engine) as session:

            statement = select(models.UserCountry).join(models.Country).where(models.UserCountry.user_id == user_id)
            country = session.exec(statement).first()
            
            return schemas.CountryResponse.model_validate(country.model_dump()) if country else None

    def set_user_country(self, user_id: int, country_id: int) -> schemas.CountryResponse:
        with Session(self.engine) as session:

            user_country = session.exec(select(models.UserCountry).where(models.UserCountry.user_id == user_id)).first()

            if user_country is None:
                user_country = models.UserCountry(user_id=user_id, country_id=country_id)
                session.add(user_country)
            else:
                user_country.country_id = country_id

            session.add(user_country)
            session.commit()
            session.refresh(user_country)

            # Get the updated country information
            statement = select(models.UserCountry).join(models.Country).where(models.UserCountry.user_id == user_id)
            updated_country = session.exec(statement).first()

            return schemas.CountryResponse.model_validate(updated_country.model_dump()) if updated_country else None
    

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
        
        # Account queries
        self.select_account_by_id_stmt = self.session.prepare("SELECT * FROM account WHERE id = ?")
        self.insert_account_stmt = self.session.prepare("INSERT INTO account (id, username, followers) VALUES (?, ?, ?)")
        
        # Publication queries
        self.select_publication_by_id_stmt = self.session.prepare("SELECT * FROM publication WHERE id = ?")
        self.insert_publication_stmt = self.session.prepare("INSERT INTO publication (id, account_id, type, insights) VALUES (?, ?, ?, ?)")
        self.select_publications_by_account_stmt = self.session.prepare("SELECT * FROM publications_by_account WHERE account_id = ?")
        
        # User Account queries
        self.select_user_account_by_id_stmt = self.session.prepare("SELECT * FROM user_account WHERE id = ?")
        self.insert_user_account_stmt = self.session.prepare("INSERT INTO user_account (id, user_id, account_id) VALUES (?, ?, ?)")
        self.select_user_accounts_by_user_stmt = self.session.prepare("SELECT * FROM user_accounts_by_user WHERE user_id = ?")
        self.select_user_accounts_by_account_stmt = self.session.prepare("SELECT * FROM user_accounts_by_account WHERE account_id = ?")
        
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

    def all_applications(self, campaign_id: int | None = None, user_id: int | None = None) -> List[schemas.CampaignApplicationResponse]:
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

    def create_user(self, id: int, user_data: schemas.UserCreate) -> schemas.UserResponse | None:
        """Create a user in ScyllaDB"""


        data = user_data.model_dump()
        self.session.execute(self.insert_user_stmt, [id, data['username'], data['email'], data['password']])
        
        
        # Return created user
        result_rows = list(self.session.execute(self.select_user_by_id_stmt, [id]))
        if not result_rows:
            return None
        row = result_rows[0]

        return schemas.UserResponse(id=row.id, username=row.username, email=row.email)

    def create_organization(self, id: int, organization_data: schemas.OrganizationCreate) -> schemas.OrganizationResponse | None:
        """Create an organization in ScyllaDB"""
        
        data = organization_data.model_dump()
        self.session.execute(self.insert_org_stmt, [id, data['name']])
        
        # Return created organization
        result_rows = list(self.session.execute(self.select_org_by_id_stmt, [id]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.OrganizationResponse(id=row.id, name=row.name)

    def create_campaign(self, id: int, campaign_data: schemas.CampaignCreate) -> schemas.CampaignResponse | None:
        """Create a campaign with requirements in ScyllaDB"""
        
        
        # Create campaign
        self.session.execute(self.insert_campaign_stmt, [id, campaign_data.organizer_id, campaign_data.name])
        
        
        # Create requirements
        requirements_list = []
        for requirement in campaign_data.requirements:
            # Fetch current requirements id
            req_current_id_result = list(self.session.execute(self.select_req_sequence_stmt, [0]))
            if not req_current_id_result:
                raise ValueError("Failed to retrieve current requirements ID")
            req_current_id = req_current_id_result[0]
            new_req_id = req_current_id[0] + 1
            
            self.session.execute(self.insert_requirement_stmt, [new_req_id, id, requirement.media_type.value, requirement.count])
            
            # Update requirements sequence
            self.session.execute(self.update_req_sequence_stmt, [new_req_id, 0])
            
            requirements_list.append(requirement)
        
        return schemas.CampaignResponse(
            id=id,
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

    def create_application(self, id: int, application_data: schemas.CampaignApplicationCreate) -> schemas.CampaignApplicationResponse | None:
        """Create a campaign application in ScyllaDB"""
        data = application_data.model_dump()
        self.session.execute(self.insert_app_stmt, [id, data['campaign_id'], data['user_id'], data['status']])
        
        # Return created application
        result_rows = list(self.session.execute(self.select_app_by_id_stmt, [id]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.CampaignApplicationResponse(
            id=row.id,
            campaign_id=row.campaign_id,
            user_id=row.user_id,
            status=row.status
        )

    # Account functions
    def create_account(self, account_data: schemas.AccountCreate) -> schemas.AccountResponse | None:
        """Create an account in ScyllaDB"""
        import uuid
        
        new_account_id = uuid.uuid4()
        
        data = account_data.model_dump()
        self.session.execute(self.insert_account_stmt, [new_account_id, data['username'], data['followers']])
        
        # Return created account
        result_rows = list(self.session.execute(self.select_account_by_id_stmt, [new_account_id]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.AccountResponse(id=row.id, username=row.username, followers=row.followers)

    def update_account(self, account_id: str, account_data: schemas.AccountUpdate) -> schemas.AccountResponse | None:
        """Update an account in ScyllaDB"""
        import uuid
        
        try:
            account_uuid = uuid.UUID(account_id)
        except ValueError:
            return None
            
        update_dict = account_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in update_dict.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        
        query = f"UPDATE account SET {', '.join(set_clauses)} WHERE id = %s"
        values.append(account_uuid)
        
        self.session.execute(query, values)
        
        # Return updated account
        result_rows = list(self.session.execute(self.select_account_by_id_stmt, [account_uuid]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.AccountResponse(id=row.id, username=row.username, followers=row.followers)

    def all_accounts(self) -> List[schemas.AccountResponse]:
        """Get all accounts from ScyllaDB"""
        query = "SELECT * FROM account"
        rows = self.session.execute(query)
        
        accounts = [schemas.AccountResponse(id=row.id, username=row.username, followers=row.followers) for row in rows]
        
        accounts.sort(key=lambda a: str(a.id))
        return accounts

    # Publication functions
    def all_publications(self, account_id: str | None = None) -> List[schemas.PublicationResponse]:
        """Get all publications from ScyllaDB, optionally filtered by account_id"""
        import json
        import uuid
        
        if account_id:
            try:
                account_uuid = uuid.UUID(account_id)
                rows = self.session.execute(self.select_publications_by_account_stmt, [account_uuid])
            except ValueError:
                return []
        else:
            query = "SELECT * FROM publication"
            rows = self.session.execute(query)

        publications = []
        for row in rows:
            try:
                # Parse JSON insights
                insights = json.loads(row.insights) if row.insights else {}
            except json.JSONDecodeError:
                insights = {}
                
            publications.append(schemas.PublicationResponse(
                id=row.id,
                account_id=row.account_id,
                type=row.type,
                insights=insights
            ))

        publications.sort(key=lambda p: str(p.id))
        return publications

    def create_publication(self, publication_data: schemas.PublicationCreate) -> schemas.PublicationResponse | None:
        """Create a publication in ScyllaDB"""
        import uuid
        import json
        
        new_publication_id = uuid.uuid4()
        
        data = publication_data.model_dump()
        insights_json = json.dumps(data['insights'])
        
        self.session.execute(self.insert_publication_stmt, [
            new_publication_id, 
            data['account_id'], 
            data['type'], 
            insights_json
        ])
        
        # Return created publication
        result_rows = list(self.session.execute(self.select_publication_by_id_stmt, [new_publication_id]))
        if not result_rows:
            return None
        row = result_rows[0]
        
        try:
            insights = json.loads(row.insights) if row.insights else {}
        except json.JSONDecodeError:
            insights = {}
            
        return schemas.PublicationResponse(
            id=row.id,
            account_id=row.account_id,
            type=row.type,
            insights=insights
        )

    def update_publication(self, publication_id: str, publication_data: schemas.PublicationUpdate) -> schemas.PublicationResponse | None:
        """Update a publication in ScyllaDB"""
        import uuid
        import json
        
        try:
            publication_uuid = uuid.UUID(publication_id)
        except ValueError:
            return None
            
        update_dict = publication_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in update_dict.items():
            if key == 'insights':
                # Convert insights dict to JSON string
                value = json.dumps(value)
            set_clauses.append(f"{key} = %s")
            values.append(value)
        
        query = f"UPDATE publication SET {', '.join(set_clauses)} WHERE id = %s"
        values.append(publication_uuid)
        
        self.session.execute(query, values)
        
        # Return updated publication
        result_rows = list(self.session.execute(self.select_publication_by_id_stmt, [publication_uuid]))
        if not result_rows:
            return None
        row = result_rows[0]
        
        try:
            insights = json.loads(row.insights) if row.insights else {}
        except json.JSONDecodeError:
            insights = {}
            
        return schemas.PublicationResponse(
            id=row.id,
            account_id=row.account_id,
            type=row.type,
            insights=insights
        )


    # User Account functions
    def all_user_accounts(self, user_id: int) -> List[schemas.UserAccountResponse]:
        """Get all user accounts from ScyllaDB for a specific user"""
        import uuid
        
        # Filter by user_id only
        rows = self.session.execute(self.select_user_accounts_by_user_stmt, [user_id])
        user_accounts = [schemas.UserAccountResponse(
            id=row.id,
            user_id=row.user_id,
            account_id=row.account_id
        ) for row in rows]

        user_accounts.sort(key=lambda ua: str(ua.id))
        return user_accounts

    def create_user_account(self, user_account_data: schemas.UserAccountCreate) -> schemas.UserAccountResponse | None:
        """Create a user account relationship in ScyllaDB"""
        import uuid
        
        new_user_account_id = uuid.uuid4()
        
        data = user_account_data.model_dump()
        self.session.execute(self.insert_user_account_stmt, [
            new_user_account_id, 
            data['user_id'], 
            data['account_id']
        ])
        
        # Return created user account
        result_rows = list(self.session.execute(self.select_user_account_by_id_stmt, [new_user_account_id]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.UserAccountResponse(id=row.id, user_id=row.user_id, account_id=row.account_id)

    def update_user_account(self, user_account_id: str, user_account_data: schemas.UserAccountUpdate) -> schemas.UserAccountResponse | None:
        """Update a user account relationship in ScyllaDB"""
        import uuid
        
        try:
            user_account_uuid = uuid.UUID(user_account_id)
        except ValueError:
            return None
            
        update_dict = user_account_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in update_dict.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        
        query = f"UPDATE user_account SET {', '.join(set_clauses)} WHERE id = %s"
        values.append(user_account_uuid)
        
        self.session.execute(query, values)
        
        # Return updated user account
        result_rows = list(self.session.execute(self.select_user_account_by_id_stmt, [user_account_uuid]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.UserAccountResponse(id=row.id, user_id=row.user_id, account_id=row.account_id)

    def get_user_account(self, user_account_id: str) -> schemas.UserAccountResponse | None:
        """Get a single user account relationship by ID"""
        import uuid
        
        try:
            user_account_uuid = uuid.UUID(user_account_id)
        except ValueError:
            return None
            
        result_rows = list(self.session.execute(self.select_user_account_by_id_stmt, [user_account_uuid]))
        if not result_rows:
            return None
        row = result_rows[0]
        return schemas.UserAccountResponse(id=row.id, user_id=row.user_id, account_id=row.account_id)

    def current_user_id(self) -> int:
        """Get the current highest user ID in ScyllaDB"""
        current_id_result = list(self.session.execute(self.select_user_sequence_stmt, [0]))
        if not current_id_result:
            raise ValueError("Failed to retrieve current user ID")
        current_id = current_id_result[0]
        return current_id[0]
    
    def current_organization_id(self) -> int:
        """Get the current highest organization ID in ScyllaDB"""
        current_id_result = list(self.session.execute(self.select_org_sequence_stmt, [0]))
        if not current_id_result:
            raise ValueError("Failed to retrieve current organization ID")
        current_id = current_id_result[0]
        return current_id[0]
    
    def current_campaign_id(self) -> int:
        """Get the current highest campaign ID in ScyllaDB"""
        current_id_result = list(self.session.execute(self.select_campaign_sequence_stmt, [0]))
        if not current_id_result:
            raise ValueError("Failed to retrieve current campaign ID")
        current_id = current_id_result[0]
        return current_id[0]
    
    def current_application_id(self) -> int:
        """Get the current highest application ID in ScyllaDB"""
        current_id_result = list(self.session.execute(self.select_app_sequence_stmt, [0]))
        if not current_id_result:
            raise ValueError("Failed to retrieve current application ID")
        current_id = current_id_result[0]
        return current_id[0]
    
    def update_user_sequence(self, new_id: int) -> None:
        """Update the user ID sequence in ScyllaDB"""
        self.session.execute(self.update_user_sequence_stmt, [new_id, 0])
    
    def update_organization_sequence(self, new_id: int) -> None:
        """Update the organization ID sequence in ScyllaDB"""
        self.session.execute(self.update_org_sequence_stmt, [new_id, 0])
    
    def update_campaign_sequence(self, new_id: int) -> None:
        """Update the campaign ID sequence in ScyllaDB"""
        self.session.execute(self.update_campaign_sequence_stmt, [new_id, 0])
    
    def update_application_sequence(self, new_id: int) -> None:
        """Update the application ID sequence in ScyllaDB"""
        self.session.execute(self.update_app_sequence_stmt, [new_id, 0])


def id_to_db(entity_id: int) -> str:
    if entity_id % 2 == 0:
        return "scylla"
    return "postgres"

def combine_list(list1: List, list2: List) -> List:
    #combine sorted lists into one sorted list
    combined = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i].id < list2[j].id:
            combined.append(list1[i])
            i += 1
        else:
            combined.append(list2[j])
            j += 1
    while i < len(list1):
        combined.append(list1[i])
        i += 1
    while j < len(list2):
        combined.append(list2[j])
        j += 1
    return combined


class Connector:
    def __init__(self):
        self.postgres_connector = SQLConnector(postgres_engine)
        self.scylla_connector = ScyllaConnector(scylla_session)

    def all_users(self) -> List[schemas.UserResponse]:
        postgres_users = self.postgres_connector.all_users()
        scylla_users = self.scylla_connector.all_users()
        return combine_list(postgres_users, scylla_users)
    
    def all_organizations(self) -> List[schemas.OrganizationResponse]:
        postgres_organizations = self.postgres_connector.all_organizations()
        scylla_organizations = self.scylla_connector.all_organizations()
        return combine_list(postgres_organizations, scylla_organizations)

    def all_countries(self) -> List[schemas.CountryResponse]:
        return self.postgres_connector.all_countries()

    def all_campaigns(self, organization_id: int | None = None) -> List[schemas.CampaignResponse]:
        if organization_id:
            db = id_to_db(organization_id) if organization_id else "postgres"

            print(f"target_db: {db}")

            if db == "postgres":
                return self.postgres_connector.all_campaigns(organization_id)
            if db == "scylla":
                return self.scylla_connector.all_campaigns(organization_id)
            
            return []

        postgres_campaigns = self.postgres_connector.all_campaigns()
        scylla_campaigns = self.scylla_connector.all_campaigns()
        return combine_list(postgres_campaigns, scylla_campaigns)

    def all_applications(self, organizer_id: int | None = None, campaign_id: int | None = None, user_id: int | None = None) -> List[schemas.CampaignApplicationResponse]:
        if campaign_id:
            if not organizer_id:
                return []
                
            db = id_to_db(organizer_id)

            if db == "postgres":
                return self.postgres_connector.all_applications(campaign_id, user_id)
            if db == "scylla":
                return self.scylla_connector.all_applications(campaign_id, user_id)

        postgres_applications = self.postgres_connector.all_applications(user_id)
        scylla_applications = self.scylla_connector.all_applications(user_id)
        return combine_list(postgres_applications, scylla_applications)

    def update_user(self, user_id: int, user_data: schemas.UserUpdate) -> schemas.UserResponse | None:
        db = id_to_db(user_id)

        if db == "postgres":
            return self.postgres_connector.update_user(user_id, user_data)
        if db == "scylla":
            return self.scylla_connector.update_user(user_id, user_data)
        return None

    def update_organization(self, organization_id: int, organization_data: schemas.OrganizationUpdate) -> schemas.OrganizationResponse | None:
        db = id_to_db(organization_id)

        if db == "postgres":
            return self.postgres_connector.update_organization(organization_id, organization_data)
        if db == "scylla":
            return self.scylla_connector.update_organization(organization_id, organization_data)
        return None

    def update_campaign(self, campaign_id: int, campaign_data: schemas.CampaignUpdate) -> schemas.CampaignResponse | None:
        db = id_to_db(campaign_id)

        if db == "postgres":
            return self.postgres_connector.update_campaign(campaign_id, campaign_data)
        if db == "scylla":
            return self.scylla_connector.update_campaign(campaign_id, campaign_data)
        return None

    def update_application(self, organizer_id: int, application_id: int, application_data: schemas.CampaignApplicationUpdate) -> schemas.CampaignApplicationResponse | None:
        db = id_to_db(organizer_id)

        if db == "postgres":
            return self.postgres_connector.update_application(application_id, application_data)
        if db == "scylla":
            return self.scylla_connector.update_application(application_id, application_data)
        return None

    def create_user(self, user_data: schemas.UserCreate) -> schemas.UserResponse | None:
        current_id = self.scylla_connector.current_user_id()
        next_id = current_id + 1
        self.scylla_connector.update_user_sequence(next_id)

        db = id_to_db(next_id)

        if db == "postgres":
            return self.postgres_connector.create_user(next_id, user_data)
        if db == "scylla":
            return self.scylla_connector.create_user(next_id,user_data)
        
        
        return None

    def create_organization(self, organization_data: schemas.OrganizationCreate) -> schemas.OrganizationResponse | None:
        current_id = self.scylla_connector.current_organization_id()
        next_id = current_id + 1
        self.scylla_connector.update_organization_sequence(next_id)

        db = id_to_db(next_id)
        

        if db == "postgres":
            return self.postgres_connector.create_organization(next_id, organization_data)
        if db == "scylla":
            return self.scylla_connector.create_organization(next_id, organization_data)
        
        
        return None

    def create_campaign(self, campaign_data: schemas.CampaignCreate) -> schemas.CampaignResponse | None:
        current_id = self.scylla_connector.current_campaign_id()
        next_id = current_id + 1
        self.scylla_connector.update_campaign_sequence(next_id)

        db = id_to_db(campaign_data.organizer_id)

        if db == "postgres":
            return self.postgres_connector.create_campaign(next_id, campaign_data)
        if db == "scylla":
            return self.scylla_connector.create_campaign(next_id, campaign_data)
        
        
        return None

    def create_application(self, organizer_id: int, application_data: schemas.CampaignApplicationCreate) -> schemas.CampaignApplicationResponse | None:
        current_id = self.scylla_connector.current_application_id()
        next_id = current_id + 1
        self.scylla_connector.update_application_sequence(next_id)

        db = id_to_db(organizer_id)

        if db == "postgres":
            return self.postgres_connector.create_application(next_id,application_data)
        if db == "scylla":
            return self.scylla_connector.create_application(next_id, application_data)
        return None

    # Account methods
    def create_account(self,  account_data: schemas.AccountCreate) -> schemas.AccountResponse | None:

        return self.scylla_connector.create_account(account_data)

    def update_account(self, account_id: str, account_data: schemas.AccountUpdate) -> schemas.AccountResponse | None:
        return self.scylla_connector.update_account(account_id, account_data)
    
    def all_accounts(self):
        return self.scylla_connector.all_accounts()

    # Publication methods
    def all_publications(self, account_id: str | None = None) -> List[schemas.PublicationResponse]:
        return self.scylla_connector.all_publications(account_id)

    def create_publication(self, publication_data: schemas.PublicationCreate) -> schemas.PublicationResponse | None:
        return self.scylla_connector.create_publication(publication_data)

    def update_publication(self, publication_id: str, publication_data: schemas.PublicationUpdate) -> schemas.PublicationResponse | None:
        return self.scylla_connector.update_publication(publication_id, publication_data)

    # User Account methods
    def all_user_accounts(self, user_id: int) -> List[schemas.UserAccountResponse]:
        return self.scylla_connector.all_user_accounts(user_id)

    def create_user_account(self, user_account_data: schemas.UserAccountCreate) -> schemas.UserAccountResponse | None:
        return self.scylla_connector.create_user_account(user_account_data)

    def update_user_account(self, user_account_id: str, user_account_data: schemas.UserAccountUpdate) -> schemas.UserAccountResponse | None:
        return self.scylla_connector.update_user_account(user_account_id, user_account_data)

    def get_user_account(self, user_account_id: str) -> schemas.UserAccountResponse | None:
        return self.scylla_connector.get_user_account(user_account_id)

    # User Country methods (Postgres only)
    def get_user_country(self, user_id: int) -> schemas.CountryResponse | None:
        """Get user's country information (Postgres only)"""
        return self.postgres_connector.get_user_country(user_id)

    def set_user_country(self, user_id: int, country_id: int) -> schemas.CountryResponse | None:
        """Set/update user's country (Postgres only)"""
        return self.postgres_connector.set_user_country(user_id, country_id)

def get_db_connector() -> Connector:
    return Connector()