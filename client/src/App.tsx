import { useState } from "react";
import './global.css'
import MarkDownDisplay from "./common/component/display/MarkdownDisplay";

function App() {
  const [analysis, setAnalysis] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [ticker, setTicker] = useState<string>('');

  const handleSubmit = async () => {

  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">SEC Filing Comparison</h1>
        <h2>Search Ticker Symbol</h2>
        <input/>
        <div className="gap-y-6">
          <button
            onClick={handleSubmit}
            disabled={loading}
            className={`w-full font-semibold py-3 px-6 rounded-lg transition duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 ${
              loading 
                ? 'bg-indigo-400 cursor-not-allowed' 
                : 'bg-indigo-600 hover:bg-indigo-700 cursor-pointer transform hover:scale-105'
            } text-white`}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing Filings...
              </span>
            ) : (
              'Compare Filings'
            )}
          </button>
        </div>
      </div>
      
      {loading && (
        <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
          <div className="flex flex-col items-center justify-center py-8">
            <svg className="animate-spin h-12 w-12 text-indigo-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="text-lg font-medium text-gray-700">Fetching and analyzing SEC filings...</p>
            <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
          </div>
        </div>
      )}
      
      {analysis && (
        <MarkDownDisplay markdown={analysis} />
      )}
      </div>
    </div>
  );
}

export default App;