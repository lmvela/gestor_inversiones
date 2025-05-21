type StockProps = {
  symbol: string;
  price: number;
  moving_average: number;
  signal: string;
};

export default function StockCard({ symbol, price, moving_average, signal }: StockProps) {
  return (
    <div className="border rounded-xl p-4 shadow-md">
      <h2 className="text-xl font-semibold">{symbol}</h2>
      <p>Price: ${price.toFixed(2)}</p>
      <p>Moving Avg: ${moving_average.toFixed(2)}</p>
      <p>Signal: <strong>{signal}</strong></p>
    </div>
  );
}
