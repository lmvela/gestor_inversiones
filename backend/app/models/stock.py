from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DailyPrice(Base):
    __tablename__ = "daily_prices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_symbol = Column(String, nullable=False)
    market = Column(String, nullable=False)  
    date = Column(Date, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    __table_args__ = (UniqueConstraint("stock_symbol", "date", name="_stock_date_uc"),)

class IntradayPrice(Base):
    __tablename__ = "intraday_prices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_symbol = Column(String, nullable=False)
    market = Column(String, nullable=False) 
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    __table_args__ = (UniqueConstraint("stock_symbol", "price", "timestamp", name="_stock_price_ts_uc"),)
