from datetime import datetime
import pandas as pd
import yfinance as yf
from curl_cffi.requests import Session
from app.models.stock import DailyPrice, IntradayPrice
from app.db.database import SessionLocal
from app.config.markets import market_info
import pytz

session = Session(impersonate="chrome", verify=False)  # Ignora SSL
session.verify = False  # Ignorar certificados SSL


def market_active(market):
    config = market_info[market]
    now_utc = datetime.utcnow()

    # Verificar si el mercado está abierto
    if now_utc.weekday() not in config["open_days"]:
        print(f"{market} cerrado hoy ({now_utc.strftime('%A')})")
        return False

    current_hour = now_utc.hour + now_utc.minute / 60
    if not (config["open_hour_utc"] <= current_hour < config["close_hour_utc"]):
        print(f"{market} fuera de horario de apertura. Hora actual UTC: {now_utc.strftime('%H:%M')}")
        return  False
    return True


def fetch_stock_price_and_store_intraday(market: str, timezone: str, symbols: list):

    if market_active(market) == False:
        return 
    
    db = SessionLocal()
    py_market_tz = pytz.timezone(timezone)

    for symbol in symbols:
        ticker = yf.Ticker(symbol, session=session)
        
        try:
            # Precio intradía real
            intraday = ticker.history(period="1d", interval="1m")
            if not intraday.empty:
                latest = intraday.iloc[-1]
                timestamp_local = intraday.index[-1]
                if timestamp_local.tzinfo is None:
                    # Hacemos consciente el timestamp según zona del mercado
                    timestamp_local = py_market_tz.localize(timestamp_local)
                timestamp_utc = timestamp_local.astimezone(pytz.UTC).replace(tzinfo=None)
                timestamp = timestamp_utc.to_pydatetime().replace(microsecond=0)
                price = latest["Close"]

                exists = db.query(IntradayPrice).filter_by(
                    stock_symbol=symbol,
                    market=market,
                    timestamp=timestamp
                ).first()

                if not exists:
                    db.add(IntradayPrice(
                        stock_symbol=symbol,
                        market=market,
                        price=price,
                        timestamp=timestamp
                    ))

            db.commit()

        except Exception as e:
            db.rollback()
            print(f"⚠️ Error al obtener intradia de {market} {symbol}: {e}")

        finally:
            db.close()

def fetch_stock_price_and_store_daily(market: str, timezone: str, symbols: list):

    db = SessionLocal()
    py_market_tz = pytz.timezone(timezone)

    for symbol in symbols:
        ticker = yf.Ticker(symbol, session=session)
        
        try:
            # Datos diarios
            history = ticker.history(period="7d", interval="1d")
            for date, row in history.iterrows():
                # date es un Timestamp de pandas, puede o no tener tzinfo
                if date.tzinfo is None:
                    # Hacer timezone-aware asignando la zona del mercado
                    date_aware = py_market_tz.localize(date)
                else:
                    date_aware = date                    
                # Convertir a UTC
                date_utc = date_aware.astimezone(pytz.UTC)
                # Extraer solo la fecha (día concreto) para guardar en DB
                market_date = date_utc.date()

                exists = db.query(DailyPrice).filter_by(
                    stock_symbol=symbol,
                    market=market,
                    date=market_date
                ).first()

                if not exists:
                    db.add(DailyPrice(
                        stock_symbol=symbol,
                        market=market,
                        date=market_date,
                        open=row["Open"],
                        high=row["High"],
                        low=row["Low"],
                        close=row["Close"],
                        volume=int(row["Volume"]) if not pd.isna(row["Volume"]) else None
                    ))
            db.commit()

        except Exception as e:
            db.rollback()
            print(f"⚠️ Error al obtener vela diaria de {market} {symbol}: {e}")

        finally:
            db.close()
