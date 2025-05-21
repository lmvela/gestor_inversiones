// components/StockCard.tsx
import React from "react";

interface StockCardProps {
  stock_symbol: string;
  market: string;
  intraday_price: number;
  intraday_timestamp: string;
  daily: {
    date: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
  } | null;
}

const StockCard: React.FC<StockCardProps> = ({
  stock_symbol,
  market,
  intraday_price,
  intraday_timestamp,
  daily,
}) => (
  <div className="bg-[#1B4332] p-5 rounded-2xl shadow">
    <h3 className="text-xl font-semibold mb-2">{stock_symbol}</h3>
    <p className="text-sm text-gray-300 mb-2">Mercado: <strong>{market}</strong></p>
    <p className="text-sm mb-2">Último precio intradía: <strong>{intraday_price}</strong></p>
    <p className="text-sm mb-4">Timestamp: {new Date(intraday_timestamp).toLocaleString()}</p>
    {daily && (
      <>
        <div className="text-sm text-gray-200 mb-1">Diario ({daily.date}):</div>
        <ul className="text-sm pl-4 space-y-1">
          <li>Open: {daily.open}</li>
          <li>High: {daily.high}</li>
          <li>Low: {daily.low}</li>
          <li>Close: {daily.close}</li>
          <li>Volumen: {daily.volume}</li>
        </ul>
      </>
    )}
  </div>
);

export default StockCard;
