export async function getStockData(symbol: string) {
  const res = await fetch(`/api/stocks/${symbol}`);
  return res.json();
}
