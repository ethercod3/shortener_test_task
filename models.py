from sqlalchemy import Column, Integer, String, DateTime, text
from sqlalchemy.sql import func
from database import Base

class UrlMap(Base):
    __tablename__ = "url_map"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(6), unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    click_count = Column(Integer, nullable=False, server_default=text("0"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())