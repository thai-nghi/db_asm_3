import fastapi
from app.db.connector import Connector, get_db_connector
router = fastapi.APIRouter()


@router.get("/users")
async def get_users(
    db: Connector = fastapi.Depends(get_db_connector)
):
    return {"users": []}