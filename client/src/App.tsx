import { useState } from "react";
import './global.css'
import SearchStock from "./common/component/SearchStock";
import type { Stock } from "./common/types/Stock";
import secService from "./service/SecService";
import MarkDownDisplay from "./common/component/display/MarkdownDisplay";
import FinDiffButton from "./common/component/FinDiffButton";

function App() {
  const [analysis, setAnalysis] = useState<string>('');
  const [selectedStock, setSelectedStock] = useState<Stock | undefined>();
  const [available10KFilings, setAvailable10KFilings] = useState<{accessionNumber:string, filingDate:string, primaryDocument:string}[]>([]);
  const [selectedFiling1, setSelectedFiling1] = useState<string>('');
  const [selectedFiling2, setSelectedFiling2] = useState<string>('');

  const handleSubmit = async () => {
    if(!selectedFiling1 || !selectedFiling2) return;
    setAnalysis('');
    const stock1 = available10KFilings.find(filing=>filing.primaryDocument === selectedFiling1);
    const stock2 = available10KFilings.find(filing=>filing.primaryDocument === selectedFiling2);
    const url1 = `https://www.sec.gov/Archives/edgar/data/${selectedStock?.cik_str}/${stock1?.accessionNumber.replace(/-/g, '')}/${selectedFiling1}`;
    const url2 = `https://www.sec.gov/Archives/edgar/data/${selectedStock?.cik_str}/${stock2?.accessionNumber.replace(/-/g, '')}/${selectedFiling2}`;
    const resp = await secService.compare10KFilings(url1, url2);
    if(resp.ok){
      const data = await resp.json();
      setAnalysis(data);
    }
  }

  const fetchAvailable10KFilings = async (cik:string) => {
    const resp = await secService.getAvailable10KFilings(cik);
    if(resp.ok){
      const data = await resp.json();
      setAvailable10KFilings(data);
    }
  }

  const onStockSelect = (stock: Stock) => {
    fetchAvailable10KFilings(stock.cik_str);
    setSelectedStock(stock);
  }
  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">SEC Filing Comparison</h1>
      <SearchStock onSelect={onStockSelect}/>
      {selectedStock && (
        <div className="mt-4 p-4 border border-gray-300 rounded-md">
          <div className="flex flex-row justify-between">
            <h1 className="font-bold text-3xl mb-2">{selectedStock.title}</h1>
            <FinDiffButton onClick={handleSubmit} disabled={!selectedFiling1 || !selectedFiling2}>
              Compare Filings
            </FinDiffButton>
          </div>
          <p><strong>Ticker:</strong> {selectedStock.ticker}</p>
          <p><strong>CIK:</strong> {selectedStock.cik_str}</p>
          <div className="w-full flex justify-between max-w-xl mx-auto">
            <select className="border border-gray-300 rounded-md p-2" value={selectedFiling1} onChange={e => setSelectedFiling1(e.target.value)}>
              <option value="">Select a filing</option>
              {available10KFilings.map(filing=>(
                <option key={filing.accessionNumber} value={filing.primaryDocument}>
                  {filing.filingDate.split('-')[0]}
                </option>
              ))}
            </select>
            <select className="border border-gray-300 rounded-md p-2" value={selectedFiling2} onChange={e=>setSelectedFiling2(e.target.value)}>
              <option value="">Select a filing</option>
              {available10KFilings.map(filing=>(
                <option key={filing.accessionNumber} value={filing.primaryDocument}>
                  {filing.filingDate.split('-')[0]}
                </option>
              ))}
            </select>
          </div>
        </div>
      )}
      {analysis && (
        <MarkDownDisplay markdown={analysis} />
      )}
    </div>
  );
}

export default App;