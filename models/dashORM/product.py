import uuid
from sqlalchemy import Boolean, Column, Index, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from config.session import Base



class ProductORM(Base):
    __tablename__ = "product"
    __table_args__ = (
        Index("product_id_index", "id"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    value = Column(Numeric(8, 2), nullable=False)
    on_offer = Column(Boolean, nullable=False)
