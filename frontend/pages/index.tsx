import { useEffect, useState } from "react";
import StockCard from "../components/StockCard";
import { getStockData } from "../utils/api";

const symbols = ["AAPL", "TSLA", "MSFT", "AMZN"];

export default function Home() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const results = await Promise.all(symbols.map(getStockData));
      setStocks(results);
    }
    fetchData();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Stock Dashboard</h1>
      <div className="grid grid-cols-2 gap-4">
        {stocks.map((stock, index) => (
          <StockCard key={index} {...stock} />
        ))}
      </div>
    </div>
  );
}
