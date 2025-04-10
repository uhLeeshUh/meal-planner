from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class BaseModel(Base):
    __abstract__ = True  # This tells SQLAlchemy this is an abstract base class
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
    
    # This ensures all subclasses must define __tablename__
    @declared_attr
    def __tablename__(cls) -> str:
        raise NotImplementedError("All models must define __tablename__") 