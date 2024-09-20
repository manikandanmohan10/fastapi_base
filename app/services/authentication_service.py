from pymongo.errors import DuplicateKeyError
from fastapi import Depends
from fastapi.exceptions import HTTPException
from app.repositories.crud import CRUDOperations
from app.schema.user_schema import SignUpSchema, LoginSchema
from app.core.password_manager import PasswordManager
from app.core.jwt_manager import JWTManager
from app.core.custom_logger import logger
from app.models.user import TabUser
from sqlalchemy.orm import Session

class AuthenticationService:
    def __init__(self, db: Session) -> None:
        self.jwt_manager = JWTManager()
        self.pw_manager = PasswordManager()
        self.db = CRUDOperations(session=db, table=TabUser)

    async def _get_user(self, email):
        user = self.db.get({'email': email})
        if not user:
            logger.error("User not found")
            raise HTTPException(status_code=400, detail="User Not found")
        return user
    
    async def _password_verification(self, pw, hashed_pw):
        if not self.pw_manager.verify_password(pw, hashed_pw):
            logger.error("password is incorrect")
            raise HTTPException(status_code=400, detail="Password is incorrect")

    async def signup(self, user_data: SignUpSchema):
        try:
            user_data.password = self.pw_manager.hash_password(user_data.password)
            user_details = dict(user_data)
            user_details['is_active'] = True
            self.db.create(user_details)
            logger.info("User created successfully")
            return {"message": "User registered successfully", "status_code": 200}
        except DuplicateKeyError as e:
            logger.error("Duplicate key, email already registered", str(e))
            raise HTTPException(status_code=400, detail="Email already registered")
        
    async def login(self, user_data: LoginSchema):
        user = await self._get_user(user_data.email)
        
        if not user['is_active']:
            logger.error("User is not active", user_data)
            raise HTTPException(status_code=400, detail="User is disabled")
        
        await self._password_verification(user_data.password, user['password'])
        
        access_token = self.jwt_manager.create_access_token({'email': user['email']})
        logger.info("User logged in & Access token generated successfully")
        return {"message": "User logged in successfully", "access_token": access_token, "type": "Bearer"}
    
    async def disable_account(self, current_user, password):
        user = await self._get_user(current_user)

        await self._password_verification(password, user['password'])
        
        self.db.update(user['email'], {'is_active': False})
        logger.info("User disabled successfully")
        return {"message": "User is disabled"}
    
    async def enable_account(self, user_data: LoginSchema):
        user = await self._get_user(user_data.email)
        if user['is_active']:
            logger.error("User already exists")
            return HTTPException(status_code=400, detail="User is already active")
        
        await self._password_verification(user_data.password, user['password'])
        
        logger.info("User enabled successfully")
        self.db.update(user['_id'], {'is_active': True})
        return {"message": "User is enabled"}
