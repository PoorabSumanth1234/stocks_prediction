const MultiPredictionPanel = ({ data }) => {
  // Handle the case where the prediction is an error message
  if (data.error) {
    return (
      <div className="w-full max-w-5xl bg-gray-800 p-4 rounded-lg">
        <h2 className="text-xl font-bold mb-2">AI Price Prediction</h2>
        <p className="text-center text-yellow-500">{data.error}</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-5xl bg-gray-800 p-4 rounded-lg">
      <h2 className="text-xl font-bold mb-4">AI Price Prediction</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
        
        {/* 1 Day Prediction */}
        <div className="bg-gray-700 p-3 rounded-md">
          <div className="text-sm text-gray-400">1 Day</div>
          <div className="text-2xl font-bold">${data['1-day']?.toFixed(2)}</div>
        </div>
        
        {/* 1 Week Prediction */}
        <div className="bg-gray-700 p-3 rounded-md">
          <div className="text-sm text-gray-400">1 Week</div>
          <div className="text-2xl font-bold">${data['1-week']?.toFixed(2)}</div>
        </div>

        {/* 1 Month Prediction */}
        <div className="bg-gray-700 p-3 rounded-md">
          <div className="text-sm text-gray-400">1 Month</div>
          <div className="text-2xl font-bold">${data['1-month']?.toFixed(2)}</div>
        </div>
        
        {/* 1 Year Prediction */}
        <div className="bg-gray-700 p-3 rounded-md">
          <div className="text-sm text-gray-400">1 Year</div>
          <div className="text-2xl font-bold">${data['1-year']?.toFixed(2)}</div>
        </div>

      </div>
      <p className="text-center text-xs text-gray-500 mt-4">{data.note}</p>
    </div>
  );
};

export default MultiPredictionPanel;