import uuid
from sqlalchemy import Column, Integer, String, Boolean, Table, UUID
from app.db.base import Base

class TabUser(Base):
    __tablename__ = 'tabUser'
    

    id = Column(Integer, primary_key=True)
    # id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    full_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)