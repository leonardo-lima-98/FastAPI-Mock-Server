import uuid
from sqlalchemy import Column, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from config import Base

class PurchaseORM(Base):
    __tablename__ = "purchase"
    __table_args__ = (
        Index("purchase_customer_id_index", "customer_id"),
        Index("purchase_product_id_index", "product_id"),
        Index("purchase_id_customer_id_product_id_index", "id", "customer_id", "product_id"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("product.id"), nullable=False)
    purchase_date = Column(Date, nullable=False)


    