from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from config import get_session
from schemas import Customer
from models import CustomerORM

router = APIRouter()

@router.get("/randon", response_model=Customer)
def get_random_user(db: Session = Depends(get_session)):
    stmt = select(CustomerORM).order_by(func.random()).limit(1)
    result = db.execute(stmt)
    customer = result.scalar_one_or_none() # extrai a linha
    if customer:
        return customer # transforma em dict compatível com Pydantic
    return {"message": "No user found"}