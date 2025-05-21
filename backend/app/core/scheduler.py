from apscheduler.schedulers.background import BackgroundScheduler
from app.services.fetcher import fetch_stock_price
from app.db.database import SessionLocal
from app.models.stock import StockPrice

SYMBOLS = ["AAPL", "TSLA", "MSFT", "AMZN"]

def fetch_and_store():
    db = SessionLocal()
    for symbol in SYMBOLS:
        price = fetch_stock_price(symbol)
        if price:
            db.add(StockPrice(symbol=symbol, price=price))
    db.commit()
    db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store, 'interval', seconds=10)
    scheduler.start()
