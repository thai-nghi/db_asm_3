import fastapi
from app.db.connector import Connector, get_db_connector
from app import schemas
from typing import Optional
router = fastapi.APIRouter()


# READ ENDPOINTS

@router.get("/users", response_model=list[schemas.UserResponse])
async def users(
    db: Connector = fastapi.Depends(get_db_connector)
) -> list[schemas.UserResponse]:
    return db.all_users()


@router.get("/organizations", response_model=list[schemas.OrganizationResponse])
async def organizations(
    db: Connector = fastapi.Depends(get_db_connector)
) -> list[schemas.OrganizationResponse]:
    return db.all_organizations()


@router.get("/countries", response_model=list[schemas.CountryResponse])
async def countries(
    db: Connector = fastapi.Depends(get_db_connector)
) -> list[schemas.CountryResponse]:
    return db.all_countries()


@router.get("/campaigns", response_model=list[schemas.CampaignResponse])
async def campaigns(
    db: Connector = fastapi.Depends(get_db_connector),
    organization_id: Optional[int] = fastapi.Query(None)
) -> list[schemas.CampaignResponse]:
    result = db.all_campaigns(organization_id)
    return result

@router.get("/applications", response_model=list[schemas.CampaignApplicationResponse])
async def campaign_applications(
    db: Connector = fastapi.Depends(get_db_connector),
    organizer_id: Optional[int] = fastapi.Query(None),
    user_id: Optional[int] = fastapi.Query(None),
    campaign_id: Optional[int] = fastapi.Query(None),
) -> list[schemas.CampaignApplicationResponse]:
    return db.all_applications(organizer_id, campaign_id, user_id)

# CREATE ENDPOINTS

@router.post("/users", response_model=schemas.UserResponse)
async def create_user(
    user_data: schemas.UserCreate,
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.UserResponse:
    result = db.create_user(user_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create user")
    return result


@router.post("/organizations", response_model=schemas.OrganizationResponse)
async def create_organization(
    organization_data: schemas.OrganizationCreate,
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.OrganizationResponse:
    result = db.create_organization(organization_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create organization")
    return result


@router.post("/campaigns", response_model=schemas.CampaignResponse)
async def create_campaign(
    campaign_data: schemas.CampaignCreate,
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.CampaignResponse:
    result = db.create_campaign(campaign_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create campaign")
    return result


@router.post("/applications", response_model=schemas.CampaignApplicationResponse)
async def create_application(
    application_data: schemas.CampaignApplicationCreate,
    organizer_id: int = fastapi.Query(...),
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.CampaignApplicationResponse:
    result = db.create_application(organizer_id, application_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create application")
    return result

# UPDATE ENDPOINTS

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: int = fastapi.Path(...),
    user_data: schemas.UserUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.UserResponse:
    result = db.update_user(user_id, user_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return result


@router.put("/organizations/{organization_id}", response_model=schemas.OrganizationResponse)
async def update_organization(
    organization_id: int = fastapi.Path(...),
    organization_data: schemas.OrganizationUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector),
) -> schemas.OrganizationResponse:
    result = db.update_organization(organization_id, organization_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="Organization not found")
    return result


@router.put("/campaigns/{campaign_id}", response_model=schemas.CampaignResponse)
async def update_campaign(
    campaign_id: int = fastapi.Path(...),
    campaign_data: schemas.CampaignUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector),
) -> schemas.CampaignResponse:
    result = db.update_campaign(campaign_id, campaign_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="Campaign not found")
    return result

@router.put("/applications/{organizer_id}/{application_id}", response_model=schemas.CampaignApplicationResponse)
async def update_application(
    organizer_id: int = fastapi.Path(...),
    application_id: int = fastapi.Path(...),
    application_data: schemas.CampaignApplicationUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector),
) -> schemas.CampaignApplicationResponse:
    result = db.update_application(organizer_id, application_id, application_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="Application not found")
    return result


# ACCOUNT ENDPOINTS (ScyllaDB only)

@router.get("/accounts", response_model=list[schemas.AccountResponse])
async def accounts(
    db: Connector = fastapi.Depends(get_db_connector)
) -> list[schemas.AccountResponse]:
    return db.all_accounts()


@router.post("/accounts", response_model=schemas.AccountResponse)
async def create_account(
    account_data: schemas.AccountCreate,
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.AccountResponse:
    result = db.create_account(account_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create account")
    return result


@router.put("/accounts/{account_id}", response_model=schemas.AccountResponse)
async def update_account(
    account_id: str = fastapi.Path(...),
    account_data: schemas.AccountUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.AccountResponse:
    result = db.update_account(account_id, account_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="Account not found")
    return result


# PUBLICATION ENDPOINTS (ScyllaDB only)

@router.get("/publications", response_model=list[schemas.PublicationResponse])
async def publications(
    db: Connector = fastapi.Depends(get_db_connector),
    account_id: Optional[str] = fastapi.Query(None)
) -> list[schemas.PublicationResponse]:
    return db.all_publications(account_id)


@router.post("/publications", response_model=schemas.PublicationResponse)
async def create_publication(
    publication_data: schemas.PublicationCreate,
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.PublicationResponse:
    result = db.create_publication(publication_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create publication")
    return result


@router.put("/publications/{publication_id}", response_model=schemas.PublicationResponse)
async def update_publication(
    publication_id: str = fastapi.Path(...),
    publication_data: schemas.PublicationUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.PublicationResponse:
    result = db.update_publication(publication_id, publication_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="Publication not found")
    return result


# USER ACCOUNT ENDPOINTS (ScyllaDB only)

@router.get("/users/{user_id}/accounts", response_model=list[schemas.UserAccountResponse])
async def user_accounts(
    user_id: int = fastapi.Path(...),
    db: Connector = fastapi.Depends(get_db_connector)
) -> list[schemas.UserAccountResponse]:
    return db.all_user_accounts(user_id)


@router.post("/user-accounts", response_model=schemas.UserAccountResponse)
async def create_user_account(
    user_account_data: schemas.UserAccountCreate,
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.UserAccountResponse:
    result = db.create_user_account(user_account_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create user account")
    return result


@router.put("/user-accounts/{user_account_id}", response_model=schemas.UserAccountResponse)
async def update_user_account(
    user_account_id: str = fastapi.Path(...),
    user_account_data: schemas.UserAccountUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.UserAccountResponse:
    result = db.update_user_account(user_account_id, user_account_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="User account not found")
    return result


@router.get("/user-accounts/{user_account_id}", response_model=schemas.UserAccountResponse)
async def get_user_account(
    user_account_id: str = fastapi.Path(...),
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.UserAccountResponse:
    result = db.get_user_account(user_account_id)
    if result is None:
        # Return empty user account response instead of 404
        return schemas.UserAccountResponse(id="", user_id=0, account_id="")
    return result


# USER COUNTRY ENDPOINTS (PostgreSQL only)

@router.get("/users/{user_id}/country", response_model=schemas.CountryResponse)
async def get_user_country(
    user_id: int = fastapi.Path(...),
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.CountryResponse:
    result = db.get_user_country(user_id)
    if result is None:
        # Return empty country response instead of 404
        return schemas.CountryResponse(id=0, code="")
    return result


@router.put("/users/{user_id}/country", response_model=schemas.CountryResponse)
async def set_user_country(
    user_id: int = fastapi.Path(...),
    country_id: int = fastapi.Body(..., embed=True),
    db: Connector = fastapi.Depends(get_db_connector)
) -> schemas.CountryResponse:
    result = db.set_user_country(user_id, country_id)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="Failed to set user country")
    return result