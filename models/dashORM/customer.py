import uuid
from sqlalchemy import Column, String, Date, Index
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from config import Base

class CustomerORM(Base):
    __tablename__ = "customer"
    __table_args__ = (
        Index("customer_id_index", "id"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    email = Column(String(255), nullable=False)
