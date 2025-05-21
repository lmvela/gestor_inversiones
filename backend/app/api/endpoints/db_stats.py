# app/api/endpoints/db_stats.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.stock import IntradayPrice
from sqlalchemy import func

router = APIRouter()

@router.get("/stats")
def get_db_stats(db: Session = Depends(get_db)):
    symbol_counts = (
        db.query(IntradayPrice.stock_symbol, func.count(IntradayPrice.id))
        .group_by(IntradayPrice.stock_symbol)
        .all()
    )
    return {
        "total_symbols": len(symbol_counts),
        "total_prices_per_symbol": {symbol: count for symbol, count in symbol_counts}
    }
