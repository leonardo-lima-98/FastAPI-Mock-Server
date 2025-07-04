from config import get_session
from depends.filters import StatsFilters
from fastapi import APIRouter, Depends, Query
from models import CustomerORM as Customer
from models import PurchaseORM as Purchase
from schemas import *
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import Optional
from uuid import UUID

router = APIRouter()

# ===== ROTAS SEPARADAS =====
@router.get("/total_customers", response_model=BaseCardResponse)
def get_total_customers(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente")
):
    """
    Retorna contagens básicas: total de compras, clientes e produtos.
    """
    filters = StatsFilters(year=year, month=month, customer_id=customer_id)
    
    # Total de clientes (considerando apenas clientes que fizeram compras nos filtros)
    if any([year, month, customer_id]):
        customer_query = select(func.count(func.distinct(Purchase.customer_id)))
        customer_query = filters.apply_purchase_filters(customer_query)
        total_customers = db.scalar(customer_query) or 0
    else:
        total_customers = db.scalar(select(func.count(Customer.id))) or 0
    
    return BaseCardResponse(
        title="Total Customers",
        value=total_customers,
        description=f"Ano: {year}, Mês {month}",
        additional_value="Count to active customers", 
        joker_param=None
    )
