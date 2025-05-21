# app/api/endpoints/markets.py
from fastapi import APIRouter
from datetime import datetime, time
import pytz
from app.config.markets import market_info

router = APIRouter()

def decimal_to_time(decimal_hour: float) -> time:
    hours = int(decimal_hour)
    minutes = int(round((decimal_hour - hours) * 60))
    return time(hour=hours, minute=minutes)

@router.get("/active")
def get_active_markets():
    now_utc = datetime.utcnow()
    active_markets = []

    for market, info in market_info.items():
        tz = pytz.timezone(info["timezone"])
        now_local = now_utc.astimezone(tz)
        weekday = now_local.weekday()

        if weekday in info["open_days"]:
            opening = decimal_to_time(info["open_hour_utc"])
            closing = decimal_to_time(info["close_hour_utc"])

            if opening <= now_local.time() <= closing:
                active_markets.append(market)

    return active_markets
