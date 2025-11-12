import fastapi
from app.db.connector import Connector, get_db_connector
from app import schemas
from typing import Optional
router = fastapi.APIRouter()


# READ ENDPOINTS

@router.get("/{db_type}/users", response_model=list[schemas.UserResponse])
async def users(
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...)
) -> list[schemas.UserResponse]:
    return db.all_users(db_type)


@router.get("/{db_type}/organizations", response_model=list[schemas.OrganizationResponse])
async def organizations(
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...)
) -> list[schemas.OrganizationResponse]:
    return db.all_organizations(db_type)


@router.get("/{db_type}/campaigns", response_model=list[schemas.CampaignResponse])
async def campaigns(
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...),
    organization_id: Optional[int] = fastapi.Query(None)
) -> list[schemas.CampaignResponse]:
    result = db.all_campaigns(db_type, organization_id)
    return result

@router.get("/{db_type}/applications", response_model=list[schemas.CampaignApplicationResponse])
async def campaign_applications(
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...),
    user_id: Optional[int] = fastapi.Query(None),
    campaign_id: Optional[int] = fastapi.Query(None),
) -> list[schemas.CampaignApplicationResponse]:
    return db.campaign_applications(db_type, campaign_id, user_id)


# CREATE ENDPOINTS

@router.post("/{db_type}/users", response_model=schemas.UserResponse)
async def create_user(
    user_data: schemas.UserCreate,
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...)
) -> schemas.UserResponse:
    result = db.create_user(db_type, user_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create user")
    return result


@router.post("/{db_type}/organizations", response_model=schemas.OrganizationResponse)
async def create_organization(
    organization_data: schemas.OrganizationCreate,
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...)
) -> schemas.OrganizationResponse:
    result = db.create_organization(db_type, organization_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create organization")
    return result


@router.post("/{db_type}/campaigns", response_model=schemas.CampaignResponse)
async def create_campaign(
    campaign_data: schemas.CampaignCreate,
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...)
) -> schemas.CampaignResponse:
    result = db.create_campaign(db_type, campaign_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create campaign")
    return result


@router.post("/{db_type}/applications", response_model=schemas.CampaignApplicationResponse)
async def create_application(
    application_data: schemas.CampaignApplicationCreate,
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...)
) -> schemas.CampaignApplicationResponse:
    result = db.create_application(db_type, application_data)
    if result is None:
        raise fastapi.HTTPException(status_code=500, detail="Failed to create application")
    return result


# UPDATE ENDPOINTS

@router.put("/{db_type}/users/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: int = fastapi.Path(...),
    user_data: schemas.UserUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...)
) -> schemas.UserResponse:
    result = db.update_user(db_type, user_id, user_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return result


@router.put("/{db_type}/organizations/{organization_id}", response_model=schemas.OrganizationResponse)
async def update_organization(
    organization_id: int = fastapi.Path(...),
    organization_data: schemas.OrganizationUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...)
) -> schemas.OrganizationResponse:
    result = db.update_organization(db_type, organization_id, organization_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="Organization not found")
    return result


@router.put("/{db_type}/campaigns/{campaign_id}", response_model=schemas.CampaignResponse)
async def update_campaign(
    campaign_id: int = fastapi.Path(...),
    campaign_data: schemas.CampaignUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...)
) -> schemas.CampaignResponse:
    result = db.update_campaign(db_type, campaign_id, campaign_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="Campaign not found")
    return result

@router.put("/{db_type}/applications/{application_id}", response_model=schemas.CampaignApplicationResponse)
async def update_application(
    application_id: int = fastapi.Path(...),
    application_data: schemas.CampaignApplicationUpdate = fastapi.Body(...),
    db: Connector = fastapi.Depends(get_db_connector),
    db_type: schemas.DatabaseType = fastapi.Path(...)
) -> schemas.CampaignApplicationResponse:
    result = db.update_application(db_type, application_id, application_data)
    if result is None:
        raise fastapi.HTTPException(status_code=404, detail="Application not found")
    return result