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
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/stocks/latest`)
      .then((res) => res.json())
      .then(setStocks);
  }, []);

  return (
    <main className="min-h-screen bg-[#0D1B2A] text-white px-6 py-12 space-y-14">
      {/* Sección 1: Mercados activos */}
      <section className="bg-[#1B263B] p-6 rounded-2xl shadow-md">
        <h2 className="text-3xl font-bold text-center text-[#4ECDC4] mb-4">Mercados Activos</h2>
        <ActiveMarkets />
      </section>

      {/* Sección 2: Acciones */}
      <section className="bg-[#1B4332] p-6 rounded-2xl shadow-md">
        <h2 className="text-3xl font-bold text-center text-[#95D5B2] mb-6">Acciones</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {stocks.map((stock) => (
            <StockCard key={stock.stock_symbol} {...stock} />
          ))}
        </div>
      </section>

      {/* Sección 3: Estadísticas de la base de datos */}
      <section className="bg-[#1B263B] p-6 rounded-2xl shadow-md">
        <h2 className="text-3xl font-bold text-center text-[#4ECDC4] mb-4">Estadísticas</h2>
        <DatabaseStats />
      </section>
    </main>
  );
}
