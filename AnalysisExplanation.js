const AnalysisExplanation = ({ data }) => {
  // This new check prevents the crash.
  // It ensures the data and the explanation text exist before trying to use them.
  if (!data || !data.explanation) {
    return null; // Render nothing if the data isn't ready
  }

  // The rest of the code runs only if the check above passes.
  const sentences = data.explanation.split('. ');

  return (
    <div className="w-full max-w-5xl bg-gray-800 p-4 rounded-lg">
      <h2 className="text-xl font-bold mb-2">Generated Analysis</h2>
      <ul className="list-disc list-inside text-gray-300 space-y-1">
        {sentences.map((sentence, index) => (
          sentence.trim() && <li key={index}>{sentence.trim()}.</li>
        ))}
      </ul>
    </div>
  );
};

export default AnalysisExplanation;