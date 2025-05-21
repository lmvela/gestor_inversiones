// components/DatabaseStats.tsx
import React, { useEffect, useState } from "react";

interface DBStats {
  total_symbols: number;
  total_prices_per_symbol: Record<string, number>;
}

const DatabaseStats = () => {
  const [stats, setStats] = useState<DBStats | null>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/db_stats/stats`).then(res => res.json()).then(setStats);
  }, []);

  return (
    <section>
      <h2 className="text-3xl font-bold text-[#4ECDC4] mb-4">Base de Datos</h2>
      {stats && (
        <>
          <p className="mb-2">Total de símbolos: <strong>{stats.total_symbols}</strong></p>
          <div className="space-y-1">
            {Object.entries(stats.total_prices_per_symbol).map(([symbol, count]) => (
              <div key={symbol} className="text-sm text-gray-300">
                {symbol}: {count} precios almacenados
              </div>
            ))}
          </div>
        </>
      )}
    </section>
  );
};

export default DatabaseStats;
