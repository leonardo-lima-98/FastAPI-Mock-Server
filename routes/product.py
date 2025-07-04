from config import get_session
from depends.filters import StatsFilters
from fastapi import APIRouter, Depends, Query
from models import PurchaseORM as Purchase
from schemas import *
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import Optional
from uuid import UUID

router = APIRouter()

# ===== ROTAS SEPARADAS =====
@router.get("/total_products", response_model=BaseCardResponse)
def get_total_products(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente")
):
    """
    Retorna contagens básicas: total de compras, clientes e produtos.
    """
    filters = StatsFilters(year=year, month=month, customer_id=customer_id)

    # Total de produtos únicos (considerando filtros)
    product_query = select(func.count(func.distinct(Purchase.product_id)))
    product_query = filters.apply_purchase_filters(product_query)
    total_products = db.scalar(product_query) or 0

    return BaseCardResponse(
        title="Total Products",
        value=total_products,
        description=f"Ano: {year}, Mês {month}",
        additional_value="Count to products purchased", 
        joker_param=None
    )
