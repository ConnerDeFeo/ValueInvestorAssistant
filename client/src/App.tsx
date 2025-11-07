import { useState } from "react";
import './global.css'
import SearchStock from "./common/component/SearchStock";
import type { Stock } from "./common/types/Stock";

function App() {
  const [analysis, setAnalysis] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedStock, setSelectedStock] = useState<Stock | undefined>();

  const handleSubmit = async () => {

  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">SEC Filing Comparison</h1>
      <SearchStock onSelect={stock=>setSelectedStock(stock)}/>
      {selectedStock && (
        <div className="mt-4 p-4 border border-gray-300 rounded-md">
          <h1 className="font-bold text-3xl mb-2">{selectedStock.title}</h1>
          <p><strong>Ticker:</strong> {selectedStock.ticker}</p>
          <p><strong>CIK:</strong> {selectedStock.cik_str}</p>
        </div>
      )}
    </div>
  );
}

export default App;