// components/StockAnalysis.js
const StockAnalysis = ({ data }) => {
  if (!data || data.currentPrice === 0) return null;

  const isPositive = data.change >= 0;
  const changeColor = isPositive ? 'text-green-500' : 'text-red-500';
  const changeSymbol = isPositive ? '▲' : '▼';

  return (
    <div className="w-full max-w-5xl bg-gray-800 p-4 rounded-lg mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Analysis</h2>
        <div>
          <span className="text-3xl font-bold">{data.currentPrice?.toFixed(2)}</span>
          <span className={`ml-4 text-xl ${changeColor}`}>
            {changeSymbol} {data.change?.toFixed(2)} ({data.percentChange?.toFixed(2)}%)
          </span>
        </div>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
        <div><span className="font-semibold text-gray-400">Open:</span> {data.openPrice?.toFixed(2)}</div>
        <div><span className="font-semibold text-gray-400">Day High:</span> {data.dayHigh?.toFixed(2)}</div>
        <div><span className="font-semibold text-gray-400">Day Low:</span> {data.dayLow?.toFixed(2)}</div>
        <div><span className="font-semibold text-gray-400">Prev. Close:</span> {data.prevClose?.toFixed(2)}</div>
      </div>
    </div>
  );
};
export default StockAnalysis;