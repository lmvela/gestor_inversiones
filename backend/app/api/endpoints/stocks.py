from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.metrics import calculate_moving_average_intraday, calculate_moving_average_daily
from app.services.signals import generate_signal
from app.models.stock import DailyPrice, IntradayPrice
from app.db.database import get_db
from typing import List, Optional

router = APIRouter()

@router.get("/stocks_intraday/{symbol}")
def get_stock_info(symbol: str, db: Session = Depends(get_db)):
    latest = db.query(IntradayPrice).filter(IntradayPrice.stock_symbol == symbol).order_by(IntradayPrice.timestamp.desc()).first()
    moving_avg = calculate_moving_average_intraday(db, symbol)
    signal = generate_signal(latest.price, moving_avg)
    return {
        "symbol": symbol,
        "price": latest.price,
        "timestamp": latest.timestamp,
        "moving_average": moving_avg,
        "signal": signal
    }

@router.get("/stocks_daily/{symbol}")
def get_stock_info(symbol: str, db: Session = Depends(get_db)):
    latest = db.query(DailyPrice).filter(DailyPrice.stock_symbol == symbol).order_by(DailyPrice.date.desc()).first()
    moving_avg = calculate_moving_average_daily(db, symbol)
    signal = generate_signal(latest.close, moving_avg)
    return {
        "symbol": symbol,
        "price": latest.close,
        "timestamp": latest.date,
        "moving_average": moving_avg,
        "signal": signal
    }

@router.get("/latest")
def get_latest_stocks(db: Session = Depends(get_db)) -> List[dict]:
    # Primero obtenemos los símbolos únicos de stocks
    stock_symbols = db.query(DailyPrice.stock_symbol).distinct().all()
    symbols = [s[0] for s in stock_symbols]

    results = []
    for symbol in symbols:
        # Obtener último precio intradía (más reciente timestamp)
        intraday = db.query(IntradayPrice)\
            .filter(IntradayPrice.stock_symbol == symbol)\
            .order_by(IntradayPrice.timestamp.desc())\
            .first()
        
        # Obtener último precio diario (más reciente date)
        daily = db.query(DailyPrice)\
            .filter(DailyPrice.stock_symbol == symbol)\
            .order_by(DailyPrice.date.desc())\
            .first()

        results.append({
            "stock_symbol": symbol,
            "market": daily.market if daily else "Unknown",  # asumiendo que market está en DailyPrice
            "intraday_price": intraday.price if intraday else None,
            "intraday_timestamp": intraday.timestamp.isoformat() if intraday else None,
            "daily": {
                "date": daily.date.isoformat(),
                "open": daily.open,
                "high": daily.high,
                "low": daily.low,
                "close": daily.close,
                "volume": daily.volume
            } if daily else None
        })

    return results