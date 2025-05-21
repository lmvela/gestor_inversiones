// components/ActiveMarkets.tsx
import React, { useEffect, useState } from "react";

const ActiveMarkets = () => {
  const [activeMarkets, setActiveMarkets] = useState<string[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/markets/active`).then(res => res.json()).then(setActiveMarkets);
  }, []);

  return (
    <section>
      <h2 className="text-3xl font-bold text-[#4ECDC4] mb-4">Mercados Activos</h2>
      <div className="flex flex-wrap gap-3">
        {activeMarkets.map(market => (
          <span
            key={market}
            className="bg-[#1B4332] text-white px-4 py-2 rounded-full shadow"
          >
            {market}
          </span>
        ))}
      </div>
    </section>
  );
};

export default ActiveMarkets;
