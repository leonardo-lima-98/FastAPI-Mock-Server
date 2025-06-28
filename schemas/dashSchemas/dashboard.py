# app/schemas/dashboard.py
from pydantic import BaseModel
from decimal import Decimal

# ---------- Summary Stats ----------
class StatsSummaryResponse(BaseModel):
    total_purchases: int
    total_purchases_value: float
    average_products_per_purchase: float
    total_customers: int
    total_purchases_current_year: int
    average_purchase_value: float  # <- este aqui
    max_products_per_purchase: int
    min_products_per_purchase: int
    total_products_current_year: int
    most_purchase_value: float     # <- este aqui
    average_purchase_per_customer: float
    average_products_per_customer: float

# ---------- Purchases by Year ----------
class YearlyPurchase(BaseModel):
    year: int
    total: int

# ---------- Purchases by Month ----------
class MonthlyPurchase(BaseModel):
    month: str
    total: int

# ---------- Ranking por Categoria ----------
class RankingCategory(BaseModel):
    category: str
    total: int

# ---------- Ranking por Produto ----------
class RankingProduct(BaseModel):
    product_name: str
    total: int

# ---------- Ranking por Cliente ----------
class RankingCustomer(BaseModel):
    customer_name: str
    total: int
