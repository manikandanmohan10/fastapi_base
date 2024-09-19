import time
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.core.custom_logger import logger

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            start_time = time.time()
            
            response = await call_next(request)

            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
        except Exception as e:
            logger.critical(str(e))
            return JSONResponse(
                status_code=400,
                content={"detail": str(e)}
            )
