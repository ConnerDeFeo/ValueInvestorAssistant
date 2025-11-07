import { useState } from "react";
import './global.css'
import secService from "./service/SecService";

function App() {
  const [analysis, setAnalysis] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [ticker, setTicker] = useState<string>('');
  const [searchResults, setSearchResults] = useState<Array<{title: string, ticker: string, cik_str:string}>>([]);

  const handleSubmit = async () => {

  }

  const handleSearchTicker = async () => {
    const resp = await secService.searchTickers(ticker);
    if(resp.ok) {
      const data = await resp.json();
      console.log(data);
      setSearchResults(data);
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">SEC Filing Comparison</h1>
      <h2>Search Ticker Symbol</h2>
      {searchResults.length > 0 && (<ul className="border border-gray-300 rounded-md p-4 mb-4 max-h-60 overflow-y-auto">
        {searchResults.map((result, index) => (
          <li key={index} className="mb-2">
            <strong>{result.ticker}</strong> - {result.title} (CIK: {result.cik_str})
          </li>
        ))}
      </ul>
      )}
      <div className="relative">
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          className="w-full border border-gray-300 rounded-md p-2"
          placeholder="Enter ticker symbol"
        />
        <img src="/images/Search.png" alt="Search" className="absolute right-4 top-2 cursor-pointer h-6 w-6" onClick={handleSearchTicker}  />
      </div>
    </div>
  );
}

export default App;