from fastapi import FastAPI

from api.endpoints import router

app = FastAPI(title='Система событий', version='0.1')
app.include_router(router=router)
