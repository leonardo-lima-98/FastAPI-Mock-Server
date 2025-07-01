from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from config import get_session
from schemas import *
from models import CustomerORM as Customer
from models import PurchaseORM as Purchase
from models import ProductORM as Product
from sqlalchemy import and_, extract, func, select
from datetime import date
from typing import Optional, List
from uuid import UUID

router = APIRouter()


# ===== CLASSE DE FILTROS =====
class StatsFilters:
    def __init__(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        customer_id: Optional[UUID] = None,
        purchase_id: Optional[UUID] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ):
        self.year = year
        self.month = month
        self.customer_id = customer_id
        self.purchase_id = purchase_id
        self.start_date = start_date
        self.end_date = end_date
    
    def apply_purchase_filters(self, query):
        """Aplica filtros na query de Purchase"""
        conditions = []       
        if self.year:
            conditions.append(extract('year', Purchase.purchase_date) == self.year)
        if self.month:
            conditions.append(extract('month', Purchase.purchase_date) == self.month)      
        if self.customer_id:
            conditions.append(Purchase.customer_id == self.customer_id)          
        if self.purchase_id:
            conditions.append(Purchase.id == self.purchase_id)       
        if self.start_date:
            conditions.append(Purchase.purchase_date >= self.start_date)       
        if self.end_date:
            conditions.append(Purchase.purchase_date <= self.end_date)       
        if conditions:
            return query.where(and_(*conditions))     
        return query


# ===== ROTAS SEPARADAS =====
@router.get("/purchase/total_purchases", response_model=BaseCardResponse)
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

@router.get("/customer/total_customers", response_model=BaseCardResponse)
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

@router.get("/product/total_products", response_model=BaseCardResponse)
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

@router.get("/purchase/total_value", response_model=BaseCardResponse)
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

@router.get("/purchase/average_value", response_model=BaseCardResponse)
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

@router.get("/purchase/most_value", response_model=BaseCardResponse)
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

@router.get("/average_products_per_purchase", response_model=BaseCardResponse)
def get_average_products_per_purchase(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente")
):
    """
    Retorna estatísticas de produtos por compra.
    """
    filters = StatsFilters(year=year, month=month, customer_id=customer_id)
    
    # Subquery para contar produtos por compra
    products_per_purchase_query = (select(func.count().label('count')).select_from(Purchase).group_by(Purchase.id))
    products_per_purchase_query = filters.apply_purchase_filters(products_per_purchase_query)
    products_per_purchase = products_per_purchase_query.subquery()
    # Estatísticas
    average_query = select(func.round(func.avg(products_per_purchase.c.count), 2).label('avg'))
    average_products_per_purchase = db.scalar(average_query) or 0

    return BaseCardResponse(
        title="Average Products of Purchase",
        value=average_products_per_purchase,
        description=f"Ano: {year}, Mês {month}",
        additional_value="Products per purchased", 
        joker_param=None
    )

@router.get("/average_purchase_per_customer", response_model=BaseCardResponse)
def get_average_purchase_per_customer(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente específico")
):
    """
    Retorna estatísticas por cliente.
    """
    filters = StatsFilters(year=year, month=month, customer_id=customer_id)
    
    # Total de compras (com filtros)
    purchase_query = select(func.count(func.distinct(Purchase.id)))
    purchase_query = filters.apply_purchase_filters(purchase_query)
    total_purchases = db.scalar(purchase_query) or 0
    
    # Total de clientes únicos (com filtros)
    customer_query = select(func.count(func.distinct(Purchase.customer_id)))
    customer_query = filters.apply_purchase_filters(customer_query)
    total_customers = db.scalar(customer_query) or 0
    
    # Calcular médias
    average_purchase_per_customer = round(
        (total_purchases / total_customers) if total_customers > 0 else 0, 2
    )
    return BaseCardResponse(
        title="Average Purchase Per Customer",
        value=average_purchase_per_customer,
        description=f"Ano: {year}, Mês {month}",
        additional_value="Average Purchase Per Customer", 
        joker_param=None
    )

@router.get("/average_products_per_customer", response_model=BaseCardResponse)
def get_average_products_per_customer(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente específico")
):
    """
    Retorna estatísticas por cliente.
    """
    filters = StatsFilters(year=year, month=month, customer_id=customer_id)
 
    # Total de clientes únicos (com filtros)
    customer_query = select(func.count(func.distinct(Purchase.customer_id)))
    customer_query = filters.apply_purchase_filters(customer_query)
    total_customers = db.scalar(customer_query) or 0
    
    # Compras por cliente
    purchases_per_customer_query = (select(func.count(Purchase.id).label('cnt')).group_by(Purchase.customer_id))
    purchases_per_customer_query = filters.apply_purchase_filters(purchases_per_customer_query)
    purchases_per_customer = purchases_per_customer_query.subquery()
    
    total_products_all_customers = db.scalar(select(func.sum(purchases_per_customer.c.cnt))) or 0

    average_products_per_customer = round(
        (total_products_all_customers / total_customers) if total_customers > 0 else 0, 2
    )
    
    return BaseCardResponse(
        title="Average Product Per Customer",
        value=average_products_per_customer,
        description=f"Ano: {year}, Mês {month}",
        additional_value="Average Purchase Per Customer", 
        joker_param=None
    )
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

@router.get("/yearly-stats", response_model=List[YearlyStatsResponse])
def get_yearly_stats(
    db: Session = Depends(get_session),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente")
):
    """
    Retorna estatísticas agrupadas por ano.
    """
    query = (
        select(
            extract('year', Purchase.purchase_date).label('year'),
            func.count(Purchase.id).label('total_purchases'),
            func.count(func.distinct(Purchase.product_id)).label('total_products'),
            func.round(func.sum(Product.value), 2).label('total_value')
        )
        .select_from(Purchase)
        .join(Product, Purchase.product_id == Product.id)
        .group_by(extract('year', Purchase.purchase_date))
        .order_by(extract('year', Purchase.purchase_date))
    )
    
    if customer_id:
        query = query.where(Purchase.customer_id == customer_id)
    
    results = db.execute(query).mappings().all()
    
    return [
        YearlyStatsResponse(
            year=int(row['year']),
            total_purchases=row['total_purchases'],
            total_products=row['total_products'],
            total_value=row['total_value'] or 0
        )
        for row in results
    ]

@router.get("/monthly-stats", response_model=List[MonthlyStatsResponse])
def get_monthly_stats(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano específico"),
    customer_id: Optional[UUID] = Query(None, description="Filtrar por ID do cliente")
):
    """
    Retorna estatísticas agrupadas por mês.
    """
    query = (
        select(
            extract('year', Purchase.purchase_date).label('year'),
            extract('month', Purchase.purchase_date).label('month'),
            func.count(Purchase.id).label('total_purchases'),
            func.round(func.sum(Product.value), 2).label('total_value')
        )
        .select_from(Purchase)
        .join(Product, Purchase.product_id == Product.id)
        .group_by(
            extract('year', Purchase.purchase_date),
            extract('month', Purchase.purchase_date)
        )
        .order_by(
            extract('year', Purchase.purchase_date),
            extract('month', Purchase.purchase_date)
        )
    )
    
    conditions = []
    if year:
        conditions.append(extract('year', Purchase.purchase_date) == year)
    if customer_id:
        conditions.append(Purchase.customer_id == customer_id)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    results = db.execute(query).mappings().all()
    
    return [
        MonthlyStatsResponse(
            year=int(row['year']),
            month=int(row['month']),
            total_purchases=row['total_purchases'],
            total_value=row['total_value'] or 0
        )
        for row in results
    ]

@router.get("/customer-ranking", response_model=List[RankingCustomerAndProduct])
def get_customer_ranking(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Número de clientes no ranking")
):
    """
    Retorna ranking de clientes por valor total de compras.
    """
    filters = StatsFilters(year=year, month=month)
    
    query = (
        select(
            Customer.id,
            Customer.first_name,
            Customer.last_name,
            Customer.email,
            func.count(Purchase.id).label('total_purchases'),
            func.round(func.sum(Product.value), 2).label('total_spent')
        )
        .select_from(Customer)
        .join(Purchase, Customer.id == Purchase.customer_id)
        .join(Product, Purchase.product_id == Product.id)
        .group_by(Customer.id, Customer.first_name, Customer.last_name)
        .order_by(func.sum(Product.value).desc())
        .limit(limit)
    )
    
    query = filters.apply_purchase_filters(query)
    
    results = db.execute(query).mappings().all()

    return [
        RankingCustomerAndProduct(
            customer_id= str(row['id']),
            first_name= str(row['first_name']),
            last_name= str(row['last_name']),
            total_purchases= row['total_purchases'],
            total_spent= row['total_spent'] or 0
        )
        for row in results
    ]

@router.get("/product-ranking", response_model=List[RankingCustomerAndProduct])
def get_product_ranking(
    db: Session = Depends(get_session),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Número de clientes no ranking")
):
    """
    Retorna ranking de clientes por valor total de compras.
    """
    filters = StatsFilters(year=year, month=month)
    
    query = (
        select(
            Customer.id,
            Customer.first_name,
            Customer.last_name,
            Customer.email,
            func.count(Purchase.id).label('total_purchases'),
            func.round(func.sum(Product.value), 2).label('total_spent')
        )
        .select_from(Customer)
        .join(Purchase, Customer.id == Purchase.customer_id)
        .join(Product, Purchase.product_id == Product.id)
        .group_by(Customer.id, Customer.first_name, Customer.last_name)
        .order_by(func.round(func.count(Purchase.id), 2).desc())
        .limit(limit)
    )
    
    query = filters.apply_purchase_filters(query)
    
    results = db.execute(query).mappings().all()

    return [
        RankingCustomerAndProduct(
            customer_id= str(row['id']),
            first_name= str(row['first_name']),
            last_name= str(row['last_name']),
            total_purchases= row['total_purchases'],
            total_spent= row['total_spent'] or 0
        )
        for row in results
    ]

# ===== EXEMPLOS DE USO =====
"""
# Obter contagens básicas sem filtros
GET /stats/basic-counts

# Obter contagens básicas filtradas por ano
GET /stats/basic-counts?year=2024

# Obter contagens básicas filtradas por ano e mês
GET /stats/basic-counts?year=2024&month=12

# Obter contagens básicas para um cliente específico
GET /stats/basic-counts?customer_id=550e8400-e29b-41d4-a716-446655440000

# Obter valores de compras com múltiplos filtros
GET /stats/purchase-values?year=2024&month=12&customer_id=550e8400-e29b-41d4-a716-446655440000

# Obter estatísticas anuais
GET /stats/yearly-stats

# Obter estatísticas mensais de um ano específico
GET /stats/monthly-stats?year=2024

# Obter ranking dos top 5 clientes
GET /stats/customer-ranking?limit=5

# Obter ranking dos clientes em um período específico
GET /stats/customer-ranking?year=2024&month=12&limit=10
"""