from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from ..database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_email = Column(String(255))
    analysis_results = Column(JSON)
    spotify_results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    payment_status = Column(String(50))
    payment_id = Column(String(255))

    # Add relationship to User
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="reports")
