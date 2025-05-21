from apscheduler.schedulers.background import BackgroundScheduler
from app.services.fetcher import fetch_stock_price_and_store_daily, fetch_stock_price_and_store_intraday
from app.config.markets import market_info

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="UTC")

    for market, config in market_info.items():
        symbols = config["symbols"]
        tz = config["timezone"]
        interval_seconds = config["interval_seconds"]
        close_hour_utc = config["close_hour_utc"]

        # Ejecuta periodicamente para precios intradia
        scheduler.add_job(
            fetch_stock_price_and_store_intraday,
            "interval",
            seconds=interval_seconds,
            args=[market, tz, symbols],
            id=f"fetch_{market}",
            name=f"Fetch for {market}",
            replace_existing=True
        )

        # Ejecuta cada día una vez para vela diaria. Una hora despues del cierre
        scheduler.add_job(
            fetch_stock_price_and_store_daily,
            trigger='cron',
            hour=int(close_hour_utc+1),
            minute=0,
            args=[market, tz, symbols], 
            id="daily_job_nyse"
        )
        
    scheduler.start()
