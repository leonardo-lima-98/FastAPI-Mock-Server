from config import get_session
from depends.filters import StatsFilters
from fastapi import APIRouter, Depends, Query
from schemas import *
from sqlalchemy.orm import Session
from routes.customer import get_total_customers
from routes.product import get_total_products
from routes.purchase import (
    get_total_purchases, 
    get_total_value, 
    get_average_value, 
    get_most_value
    )
from routes.stats import (
    get_average_products_per_customer,
    get_average_products_per_purchase, 
    get_average_purchase_per_customer
    )
from typing import Optional
from uuid import UUID

router = APIRouter()

# ===== ROTA PARA OBTER TODOS OS DADOS DOS CARDS =====
@router.get("/summary")
def get_complete_stats_summary(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente"),
    purchase_id: Optional[UUID] = Query(None, description="Filtrar por ID da compra")
):
    """
    Retorna todas as métricas em uma única resposta (mantém compatibilidade).
    """
    # Simula chamadas internas (você pode otimizar isso)
    total_purchases = get_total_purchases(db, year, month, customer_id)
    total_customers = get_total_customers(db, year, month, customer_id)
    total_products = get_total_products(db, year, month, customer_id)
    total_value = get_total_value(db, year, month, customer_id, purchase_id)
    average_value = get_average_value(db, year, month, customer_id)
    most_value = get_most_value(db, year, month, customer_id)
    average_products_per_purchase = get_average_products_per_purchase(db, year, month, customer_id)
    average_purchase_per_customer = get_average_purchase_per_customer(db, year, month, customer_id)
    average_products_per_customer = get_average_products_per_customer(db, year, month, customer_id)
    
    return [
        total_purchases,
        total_customers,
        total_products,
        total_value,
        average_value,
        most_value,
        average_products_per_purchase,
        average_purchase_per_customer,
        average_products_per_customer
    ]
