// pages/index.tsx
import ActiveMarkets from "@/components/ActiveMarkets";
import StockCard from "@/components/StockCard";
import DatabaseStats from "@/components/DatabaseStats";
import { useEffect, useState } from "react";

interface StockData {
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

export default function Home() {
  const [stocks, setStocks] = useState<StockData[]>([]);
  console.log("API URL:", process.env.NEXT_PUBLIC_API_URL);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/stocks/latest`).then(res => res.json()).then(setStocks);
  }, []);

  return (
    <main className="min-h-screen bg-[#0D1B2A] text-white px-6 py-10 space-y-10">
      <ActiveMarkets />
      <section>
        <h2 className="text-3xl font-bold text-[#4ECDC4] mb-6">Acciones</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {stocks.map(stock => (
            <StockCard key={stock.stock_symbol} {...stock} />
          ))}
        </div>
      </section>
      <DatabaseStats />
    </main>
  );
}
