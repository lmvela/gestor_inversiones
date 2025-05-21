from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.metrics import calculate_moving_average
from app.services.signals import generate_signal
from app.models.stock import StockPrice

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stocks/{symbol}")
def get_stock_info(symbol: str, db: Session = Depends(get_db)):
    latest = db.query(StockPrice).filter(StockPrice.symbol == symbol).order_by(StockPrice.timestamp.desc()).first()
    moving_avg = calculate_moving_average(db, symbol)
    signal = generate_signal(latest.price, moving_avg)
    return {
        "symbol": symbol,
        "price": latest.price,
        "timestamp": latest.timestamp,
        "moving_average": moving_avg,
        "signal": signal
    }
