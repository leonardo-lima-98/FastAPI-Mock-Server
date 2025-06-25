
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import RedirectResponse
import psycopg2
from app.config import settings

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to the API", "status": status.HTTP_200_OK}

@router.get("/info")
async def info():
    return {
        "name": "FastAPI Example",
        "description": "This is a sample FastAPI application",
        "version": settings.API_VERSION,
        "status": status.HTTP_200_OK
    }

@router.get("/mock")
async def mock_endpoint():
    return RedirectResponse(url="/mock/data", status_code=302)

@router.get("/mock/data")
async def get_mock_data():
    return {"message": "This is mock data", "status": status.HTTP_200_OK}

@router.get("/health")
async def health_check():
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        conn.close()
        return {"database": "connected", "status": status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"database": "disconnected", "error": str(e)}
        )