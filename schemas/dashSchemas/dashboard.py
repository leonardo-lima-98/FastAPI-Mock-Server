# app/schemas/dashboard.py
from typing import Any, Optional
from pydantic import BaseModel

# ---------- Summary Stats ----------
class StatsSummaryResponse(BaseModel):
    total_purchases: int
    total_customers: int
    total_products: int
    total_purchases_value: float
    average_products_per_purchase: float
    total_purchases_current_year: int
    average_purchase_value: float  # <- este aqui
    max_products_per_purchase: int
    min_products_per_purchase: int
    total_products_current_year: int
    most_purchase_value: float     # <- este aqui
    average_purchase_per_customer: float
    average_products_per_customer: float

# ---------- Ranking por Cliente e Produto ----------
class RankingCustomerAndProduct(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    total_purchases: float
    total_spent: float

class BasicCountsResponse(BaseModel):
    total_purchases: int
    total_customers: int
    total_products: int

class PurchaseValuesResponse(BaseModel):
    total_purchases_value: float
    average_purchase_value: float
    most_purchase_value: float

class ProductsPerPurchaseResponse(BaseModel):
    average_products_per_purchase: float
    max_products_per_purchase: int
    min_products_per_purchase: int

class CustomerStatsResponse(BaseModel):
    average_purchase_per_customer: float
    average_products_per_customer: float

class YearlyStatsResponse(BaseModel):
    year: int
    total_purchases: int
    total_products: int
    total_value: float

class MonthlyStatsResponse(BaseModel):
    month: int
    year: int
    total_purchases: int
    total_value: float

class BaseCardResponse(BaseModel):
    title: str
    value: int | float
    description: str | None
    additional_value: str | None
    joker_param: str | None