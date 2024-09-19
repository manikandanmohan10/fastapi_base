from pymongo.errors import DuplicateKeyError
from fastapi.exceptions import HTTPException
from app.repositories.crud import CRUDOperations
from app.schema.user_schema import SignUpSchema, LoginSchema
from app.core.password_manager import PasswordManager
from app.core.jwt_manager import JWTManager


class AuthenticationService:
    def __init__(self) -> None:
        self.jwt_manager = JWTManager()
        self.pw_manager = PasswordManager()
        self.db = CRUDOperations("users")

    async def _get_user(self, email):
        user = self.db.get({'email': email})
        if not user:
            raise HTTPException(status_code=400, detail="User Not found")
        return user

    async def signup(self, user_data: SignUpSchema):
        try:
            user_data.password = self.pw_manager.hash_password(user_data.password)
            user_details = dict(user_data)
            user_details['is_active'] = True
            self.db.create(user_details)
            
            return {"message": "User registered successfully", "status_code": 200}
        except DuplicateKeyError as e:
            raise HTTPException(status_code=400, detail="Email already registered")
        
    async def login(self, user_data: LoginSchema):
        user = await self._get_user(user_data.email)
        
        if not user['is_active']:
            raise HTTPException(status_code=400, detail="User is disabled")
        
        if not self.pw_manager.verify_passwordd(user_data.password, user['password']):
            raise HTTPException(status_code=400, detail="Password is incorrect")
        
        access_token = self.jwt_manager.create_access_token({'email': user['email']})
        return {"message": "User logged in successfully", "access_token": access_token, "type": "Bearer"}
    
    async def disable_account(self, current_user, password):
        user = await self._get_user(current_user)
        self.db.update(user['_id'], {'is_active': False})

        return {"message": "User is disabled"}
    
    async def enable_account(self, user_data: LoginSchema):
        user = await self._get_user(user_data.email)
        if user['is_active']:
            return HTTPException(status_code=400, detail="User is already active")
        
        if not self.pw_manager.verify_password(user_data.password, user['password']):
            raise HTTPException(status_code=400, detail="Password is incorrect")

        self.db.update(user['_id'], {'is_active': True})
        return {"message": "User is enabled"}
