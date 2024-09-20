from fastapi import HTTPException
from bson import ObjectId
from typing import Any, Dict, List, Type
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from app.db.base import Base

class CRUDOperations:
    def __init__(self, session: Session, table: Type[Base]):
        self.session = session
        self.table = table

    def create(self, data: Dict) -> str:
        """Insert a new document into the collection."""
        result = self.table(**dict(data))
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)

        return str(result.id)

    def get(self, search_criteria: str) -> Dict:
        query = self.session.query(self.table)
        for key, value in search_criteria.items():
            query = query.filter(getattr(self.table, key) == value)
        data = query.first()
        if not data:
            raise HTTPException(status_code=404, detail="No data found")
        return self.to_dict(data)

    def get_all(self, filters: Dict = {}) -> List[Dict]:
        """Get all documents, optionally filtered."""
        return list(self.collection.find(filters))

    def update(self, email: str, update_data: Dict) -> Any:
        """Update a document by its ID."""
        result = self.session.query(self.table).filter(self.table.email == email).first()
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        result['is_active'] = False
        self.session.commit()

        return "Modified successfully"

    def to_dict(self, obj):
        """Convert SQLAlchemy model instance to dictionary."""
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}