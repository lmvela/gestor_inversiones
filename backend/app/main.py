from fastapi import FastAPI
from app.api.endpoints import stocks
from app.core.scheduler import start_scheduler
from app.db.database import init_db

app = FastAPI()
app.include_router(stocks.router, prefix="/api")

@app.on_event("startup")
def startup():
    init_db()
    start_scheduler()

@app.get("/")
def read_root():
    return {"message": "API de gestor de inversiones funcionando"}
