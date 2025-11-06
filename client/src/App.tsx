import { useState } from "react";
import API from "./service/API";
import ReactMarkdown from 'react-markdown';
import './global.css'

function App() {
  const [firstUrl, setFirstUrl] = useState<string>('https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm');
  const [secondUrl, setSecondUrl] = useState<string>('https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm');
  const [analysis, setAnalysis] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async () => {
    setLoading(true);
    setAnalysis(''); // Clear previous analysis
    try {
      const resp  = await API.post(`${import.meta.env.VITE_API_URL}/compare_filings`, {
        url1: firstUrl,
        url2: secondUrl
      });
      if(resp.ok) {
        const data = await resp.json();
        console.log("API response data:", data);
        setAnalysis(data.analysis);
      } else {
        console.error("API request failed with status:", resp.status);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">SEC Filing Comparison</h1>
        
        <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Older Filing URL
          </label>
          <input
          type="text"
          placeholder="Enter first URL"
          value={firstUrl}
          onChange={(e) => setFirstUrl(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition duration-200"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
          Newer Filing URL
          </label>
          <input
          type="text"
          placeholder="Enter second URL"
          value={secondUrl}
          onChange={(e) => setSecondUrl(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition duration-200"
          />
        </div>
        
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
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center border-b pb-2 border-gray-300">Analysis</h2>
          <ReactMarkdown
            components={{
              h1: ({node, ...props}) =><h1 className="text-2xl text-purple-500 font-bold my-6" {...props}></h1>,
              h2: ({node, ...props}) =><h2 className="text-xl text-purple-500 font-bold my-4" {...props}></h2>,
              h3: ({node, ...props}) =><h3 className="text-lg text-purple-500 font-bold my-3" {...props}></h3>,
              p: ({node, ...props}) =><p className="my-2 leading-7 text-gray-800" {...props}></p>,
              li: ({node, ...props}) =><li className="list-disc list-inside my-1" {...props}></li>,
            }}
          >
            {analysis}
          </ReactMarkdown>
        </div>
      )}
      </div>
    </div>
  );
}

export default App;