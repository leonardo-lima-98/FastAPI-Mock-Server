from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config import get_session
from schemas import StatsSummaryResponse
from time import time
from models import CustomerORM as Customer
from models import PurchaseORM as Purchase
from models import ProductORM as Product
from sqlalchemy import func, select

router = APIRouter()

@router.get("/summary", response_model=StatsSummaryResponse)
def get_stats_summary(db: Session = Depends(get_session)):
    """
    Retorna métricas gerais do dashboard como totais e médias.
    """
    init_time = time() # variavel para monitorar o tempo de execução
    # Abordagem 1: Usando subqueries com SQLAlchemy
    current_year_start = func.date_trunc('year', func.current_date())
    
    # Contagens básicas
    total_purchases = db.scalar(select(func.count(Purchase.id)))
    total_customers = db.scalar(select(func.count(Customer.id)))
    
    # Valor total das compras
    total_purchases_value = db.scalar(
        select(func.round(func.sum(Product.value), 2))
        .select_from(Purchase)
        .join(Product, Purchase.product_id == Product.id)
    ) or 0
    
    # Valor médio das compras
    average_purchase_value = db.scalar(
        select(func.round(func.avg(Product.value), 2))
        .select_from(Purchase)
        .join(Product, Purchase.product_id == Product.id)
    ) or 0
    
    # Subquery para contagem de produtos por compra
    products_per_purchase = (
        select(func.count().label('count'))
        .select_from(Purchase)
        .group_by(Purchase.id)
        .subquery()
    )
    
    # Estatísticas de produtos por compra
    average_products_per_purchase = db.scalar(
        select(func.round(func.avg(products_per_purchase.c.count), 2))
    ) or 0
    
    max_products_per_purchase = db.scalar(
        select(func.max(products_per_purchase.c.count))
    ) or 0
    
    min_products_per_purchase = db.scalar(
        select(func.min(products_per_purchase.c.count))
    ) or 0
    
    # Compras do ano atual
    total_purchases_current_year = db.scalar(
        select(func.count(Purchase.id))
        .where(Purchase.purchase_date >= current_year_start)
    ) or 0
    
    # Produtos únicos vendidos no ano atual
    total_products_current_year = db.scalar(
        select(func.count(func.distinct(Purchase.product_id)))
        .where(Purchase.purchase_date >= current_year_start)
    ) or 0
    
    # Valor da compra mais cara
    purchase_values = (
        select(func.sum(Product.value).label('total_value'))
        .select_from(Purchase)
        .join(Product, Purchase.product_id == Product.id)
        .group_by(Purchase.id)
        .subquery()
    )
    
    most_purchase_value = db.scalar(
        select(func.max(purchase_values.c.total_value))
    ) or 0
    
    # Média de compras por cliente
    average_purchase_per_customer = round(
        (total_purchases / total_customers) if total_customers > 0 else 0, 2
    )
    
    # Produtos por cliente (média)
    purchases_per_customer = (
        select(func.count(Purchase.id).label('cnt'))
        .group_by(Purchase.customer_id)
        .subquery()
    )
    
    total_products_all_customers = db.scalar(
        select(func.sum(purchases_per_customer.c.cnt))
    ) or 0
    
    average_products_per_customer = round(
        (total_products_all_customers / total_customers) if total_customers > 0 else 0, 2
    )
    print(f"{time() - init_time} tempo de execução em segundos") # variavel para monitorar o tempo de execução
    return StatsSummaryResponse(
        total_purchases=total_purchases,
        total_purchases_value=total_purchases_value,
        total_customers=total_customers,
        average_products_per_purchase=average_products_per_purchase,
        max_products_per_purchase=max_products_per_purchase,
        min_products_per_purchase=min_products_per_purchase,
        average_purchase_value=average_purchase_value,
        total_purchases_current_year=total_purchases_current_year,
        total_products_current_year=total_products_current_year,
        most_purchase_value=most_purchase_value,
        average_purchase_per_customer=average_purchase_per_customer,
        average_products_per_customer=average_products_per_customer
    )