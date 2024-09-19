from pymongo.errors import DuplicateKeyError
from fastapi.exceptions import HTTPException
from app.repositories.crud import CRUDOperations
from app.schema.user_schema import SignUpSchema
from app.core.password_manager import PasswordManager


class AuthenticationService:
    def __init__(self) -> None:
        self.pw_manager = PasswordManager()
        self.db = CRUDOperations("users")

    async def signup(self, user_data: SignUpSchema):
        try:
            # if self.db.get(user_data.email):
            #     raise HTTPException(status_code=400, detail="User already exists")
            
            user_data.password = self.pw_manager.hash_password(user_data.password)
            self.db.create(dict(user_data))
            
            return {"message": "User registered successfully", "status_code": 200}
        except DuplicateKeyError as e:
            raise HTTPException(detail=str(e), status_code=400)