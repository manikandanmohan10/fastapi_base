from fastapi import FastAPI
from app.core.custom_middleware import CustomMiddleware
from app.routes.user import user_router
from app.db.base import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(CustomMiddleware)
app.include_router(user_router)

@app.get('/')
def root():
    return {
        'message': 'hello world'
    }