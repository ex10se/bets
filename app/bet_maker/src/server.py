from fastapi import FastAPI

from api.public_endpoints import router as public_router
from api.service_endpoints import router as service_router

app = FastAPI()
app.include_router(router=public_router, prefix='/api')
app.include_router(router=service_router, prefix='/service')
