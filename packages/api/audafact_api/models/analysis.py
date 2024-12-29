from sqlalchemy import Column, String, JSON, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from database import Base

class UserAnalysis(Base):
    __tablename__ = "user_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=True)
    analysis_id = Column(String, nullable=False)
    partial_results = Column(JSON, nullable=True)
    has_paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
