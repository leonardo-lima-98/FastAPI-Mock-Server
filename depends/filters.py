from models import PurchaseORM as Purchase
from sqlalchemy import and_, extract
from datetime import date
from typing import Optional
from uuid import UUID

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
