from config import get_session
from depends.filters import StatsFilters
from fastapi import APIRouter, Depends, Query
from models import PurchaseORM as Purchase
from models import ProductORM as Product
from schemas import *
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import Optional
from uuid import UUID

router = APIRouter()

# ===== ROTAS SEPARADAS =====
@router.get("/total_purchases", response_model=BaseCardResponse)
def get_total_purchases(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente")
):
    """
    Retorna contagens básicas: total de compras, clientes e produtos.
    """
    filters = StatsFilters(year=year, month=month, customer_id=customer_id)
    
    # Total de compras (com filtros)
    purchase_query = select(func.count(func.distinct(Purchase.id)))
    purchase_query = filters.apply_purchase_filters(purchase_query)
    total_purchases = db.scalar(purchase_query) or 0
    
    return BaseCardResponse(
        title="Total Purchases",
        value=total_purchases,
        description=f"Ano: {year}, Mês {month}",
        additional_value="Count to effective purchases", 
        joker_param=None
    )

@router.get("/total_value", response_model=BaseCardResponse)
def get_total_value(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente"),
    purchase_id: Optional[UUID] = Query(None, description="Filtrar por ID da compra")
):
    filters = StatsFilters(year=year, month=month, customer_id=customer_id, purchase_id=purchase_id)

    # Total de valores
    total_query = select(func.round(func.sum(Product.value), 2)).select_from(Purchase).join(Product)
    total_query = filters.apply_purchase_filters(total_query)
    total_value = db.scalar(total_query) or 0

    return BaseCardResponse(
        title="Total Value of Purchase",
        value=total_value,
        description=f"Ano: {filters.year}, Mês {filters.month}",
        additional_value="Total to purchased", 
        joker_param=None
    )

@router.get("/average_value", response_model=BaseCardResponse)
def get_average_value(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente")
):
    filters = StatsFilters(year=year, month=month, customer_id=customer_id)

    # Média de valores
    average_query = select(func.round(func.avg(Product.value), 2)).select_from(Purchase).join(Product)
    average_query = filters.apply_purchase_filters(average_query)
    average_value = db.scalar(average_query) or 0

    return BaseCardResponse(
        title="Average Value of Purchase",
        value=average_value,
        description=f"Ano: {year}, Mês {month}",
        additional_value="Average value purchased", 
        joker_param=None
    )

@router.get("/most_value", response_model=BaseCardResponse)
def get_most_value(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente")
):
    filters = StatsFilters(year=year, month=month, customer_id=customer_id)

    # Maior valor de uma compra (agrupado por Purchase.id)
    purchase_totals = (select(func.sum(Product.value).label('total_value'))
        .select_from(Purchase).join(Product).group_by(Purchase.id))
    purchase_totals = filters.apply_purchase_filters(purchase_totals).subquery()
    most_value = db.scalar(select(func.max(purchase_totals.c.total_value))) or 0

    return BaseCardResponse(
        title="Most Value of Purchase",
        value=most_value,
        description=f"Ano: {year}, Mês {month}",
        additional_value="Most value purchased", 
        joker_param=None
    )
