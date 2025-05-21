from sqlalchemy.orm import Session
from app.models.stock import StockPrice
from statistics import mean

def calculate_moving_average(db: Session, symbol: str, days: int = 5) -> float:
    prices = db.query(StockPrice).filter(StockPrice.symbol == symbol).order_by(StockPrice.timestamp.desc()).limit(days).all()
    return mean([p.price for p in prices]) if prices else None
