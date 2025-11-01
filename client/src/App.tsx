import { useState } from "react";
import API from "./service/API";
import ReactMarkdown from 'react-markdown';
import './global.css'

function App() {
  const [firstUrl, setFirstUrl] = useState<string>('https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm');
  const [secondUrl, setSecondUrl] = useState<string>('https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm');
  const [analysis, setAnalysis] = useState<string>('');

  const handleSubmit = async () => {
    const resp  = await API.post("http://127.0.0.1:8000/compare", {
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
          className="cursor-pointer w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          Compare Filings
        </button>
        </div>
      </div>
      
      {analysis && (
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center border-b pb-2 border-gray-300">Analysis</h2>
          <ReactMarkdown
            components={{
              h1: ({node, ...props}) =><h1 className="text-2xl font-bold my-6" {...props}></h1>,
              h2: ({node, ...props}) =><h2 className="text-xl font-bold my-4" {...props}></h2>,
              h3: ({node, ...props}) =><h3 className="text-lg font-bold my-3" {...props}></h3>,
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