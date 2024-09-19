from pymongo import MongoClient
from bson import ObjectId
from typing import Any, Dict, List
from app.db.mongo_db import db

class CRUDOperations:
    def __init__(self, collection_name: str):
        self.collection = db[collection_name]

    def create(self, data: Dict) -> str:
        """Insert a new document into the collection."""
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def get(self, search_criteria: str) -> Dict:
        if "_id" in search_criteria and isinstance(search_criteria["_id"], str):
            # Convert the _id string to ObjectId if searching by _id
            search_criteria["_id"] = ObjectId(search_criteria["_id"])
        
        return self.collection.find_one(search_criteria)

    def get_all(self, filters: Dict = {}) -> List[Dict]:
        """Get all documents, optionally filtered."""
        return list(self.collection.find(filters))

    def update(self, document_id: str, update_data: Dict) -> Any:
        """Update a document by its ID."""
        result = self.collection.update_one(
            {"_id": ObjectId(document_id)}, {"$set": update_data}
        )
        return result.modified_count

    def delete(self, document_id: str) -> Any:
        """Delete a document by its ID."""
        result = self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count
