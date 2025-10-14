const PredictionPanel = ({ data }) => {
  // Don't render the component if there's no data
  if (!data) return null;

  return (
    <div className="w-full max-w-5xl bg-gray-800 p-4 rounded-lg text-center">
      <h2 className="text-lg font-semibold text-gray-400 mb-2">
        AI Price Prediction (Next Day)
      </h2>
      {data.predictedPrice && (
        <>
          <p className="text-4xl font-bold text-cyan-400">
            ${data.predictedPrice.toFixed(2)}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Based on historical trends from the LSTM model.
          </p>
        </>
      )}
      {data.error && (
        <p className="text-md text-amber-500">
          {data.error}
        </p>
      )}
    </div>
  );
};

export default PredictionPanel;
