from fastapi import FastAPI
from app.api.endpoints import stocks, markets, db_stats
from app.core.scheduler import start_scheduler
from app.db.database import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(markets.router, prefix="/api/markets")
app.include_router(stocks.router, prefix="/api/stocks")
app.include_router(db_stats.router, prefix="/api/db_stats")

# Configurar orígenes permitidos
origins = [
    "http://localhost:3000",  # Next.js en desarrollo
]

# Añadir el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Permitir solo localhost:3000
    allow_credentials=True,
    allow_methods=["*"],               # Permitir todos los métodos HTTP
    allow_headers=["*"],               # Permitir todos los headers
)

@app.on_event("startup")
def startup():
    init_db()
    start_scheduler()

@app.get("/")
def read_root():
    return {"message": "API de gestor de inversiones funcionando"}
