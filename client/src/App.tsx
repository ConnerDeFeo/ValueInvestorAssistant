import { useEffect, useState } from "react";
import './global.css'
import SearchStock from "./common/component/SearchStock";
import type { Stock } from "./common/types/Stock";
import secService from "./service/SecService";
import MarkDownDisplay from "./common/component/display/MarkdownDisplay";
import FinDiffButton from "./common/component/FinDiffButton";
import Spinner from "./common/component/display/Spinner";
import { Sections } from "./common/variables/Sections";

function App() {
  const [analysis, setAnalysis] = useState<string>('');
  const [jobId, setJobId] = useState<string>('');
  const [selectedStock, setSelectedStock] = useState<Stock | undefined>();
  const [available10KFilings, setAvailable10KFilings] = useState<{accessionNumber:string, filingDate:string, primaryDocument:string}[]>([]);
  const [selectedOlderFilingDate, setSelectedOlderFilingDate] = useState<string>('');
  const [selectedNewerFilingDate, setSelectedNewerFilingDate] = useState<string>('');
  const [awaitingAnalysis, setAwaitingAnalysis] = useState<boolean>(false);
  const [selectedSections, setSelectedSections] = useState<string[]>([]);

  const handleCheckboxChange = (section: string) => {
    if (selectedSections.includes(section)) {
      setSelectedSections(selectedSections.filter(s => s !== section));
    } else {
      setSelectedSections([...selectedSections, section]);
    }
  };

  const handleSubmit = async () => {
    if(!selectedOlderFilingDate || !selectedNewerFilingDate) return;
    setAnalysis('');

    const stock1 = available10KFilings.find(filing=>filing.filingDate === selectedOlderFilingDate);
    const stock2 = available10KFilings.find(filing=>filing.filingDate === selectedNewerFilingDate);
    const url1 = `https://www.sec.gov/Archives/edgar/data/${selectedStock?.cik_str}/${stock1?.accessionNumber.replace(/-/g, '')}/${stock1?.primaryDocument}`;
    const url2 = `https://www.sec.gov/Archives/edgar/data/${selectedStock?.cik_str}/${stock2?.accessionNumber.replace(/-/g, '')}/${stock2?.primaryDocument}`;
    const resp = await secService.compare10KFilings(url1, url2, selectedSections);

    if(resp.ok){
      const jobId = await resp.json();
      setJobId(jobId);
    }
  }

  useEffect(()=>{
    const poll = async (attempt: number) => {
      if (attempt >= 45) {
        setAnalysis('Analysis timed out. Please try again later.');
        setAwaitingAnalysis(false);
        return;
      }
      setAwaitingAnalysis(true);
      const resp = await secService.getComparisonStatus(jobId);
      if(!resp.ok) {
        setAnalysis('Error fetching comparison status.');
        setAwaitingAnalysis(false);
        return;
      }
      const job =  await resp.json();

      if (job.status === 'COMPLETED' || job.status === 'FAILED') {
        setAnalysis(job.result || 'Comparison failed.');
        setAwaitingAnalysis(false);
        return;
      }

      await new Promise(resolve => setTimeout(resolve, 2000));
      poll(attempt + 1);
    };
    if(jobId){
      poll(0);
      setJobId('');
    }
  }, [jobId]);

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
    <div className="min-h-screen findiff-bg-white">
      <div className="max-w-5xl mx-auto p-6 pt-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-3 bg-gradient-to-r findiff-primary-blue bg-clip-text text-transparent">
            FinDiff
          </h1>
          <p className="text-lg text-gray-600">SEC Filing Comparison & Analysis</p>
        </div>

        {/* Search Section */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6 border-t-4 findiff-border-primary-blue">
          <SearchStock onSelect={onStockSelect}/>
        </div>

        {/* Selected Stock Card */}
        {selectedStock && (
          <div className="bg-white rounded-xl shadow-lg p-8 mb-6 border-t-4 findiff-border-primary-blue">
            <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-6">
              <div>
                <h2 className="font-bold text-3xl mb-3 findiff-secondary-blue">{selectedStock.title}</h2>
                <div className="space-y-1">
                  <p className="text-gray-700">
                    <span className="font-semibold findiff-primary-blue">Ticker:</span> 
                    <span className="ml-2 px-3 py-1 bg-blue-100 findiff-primary-blue rounded-md font-mono">{selectedStock.ticker}</span>
                  </p>
                  <p className="text-gray-700">
                    <span className="font-semibold findiff-primary-blue">CIK:</span> 
                    <span className="ml-2 font-mono text-gray-600">{selectedStock.cik_str}</span>
                  </p>
                </div>
              </div>
              <FinDiffButton onClick={handleSubmit} disabled={!selectedOlderFilingDate || !selectedNewerFilingDate || awaitingAnalysis}>
                Compare Filings
              </FinDiffButton>
            </div>

            {/* Filing Selection */}
            <div className="border-t border-gray-200 pt-6">
              <h3 className="text-lg font-semibold findiff-secondary-blue mb-4 text-center">Select Two 10-K Filings to Compare</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Older Filing</label>
                  <select 
                    className="w-full border-2 border-gray-300 rounded-lg p-3 cursor-pointer hover:border-blue-500 focus:border-blue-800 focus:ring-2 focus:ring-blue-200 transition-all" 
                    value={selectedOlderFilingDate} 
                    onChange={e => setSelectedOlderFilingDate(e.target.value)}
                  >
                    <option value="" className="cursor-pointer">Select a filing</option>
                    {available10KFilings.map(filing=> (!selectedNewerFilingDate || filing.filingDate < selectedNewerFilingDate) && (
                      <option key={filing.accessionNumber} value={filing.filingDate} className="cursor-pointer">
                        {filing.filingDate.split('-')[0]}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Newer Filing</label>
                  <select 
                    className="w-full border-2 border-gray-300 rounded-lg p-3 cursor-pointer hover:border-blue-500 focus:border-blue-800 focus:ring-2 focus:ring-blue-200 transition-all" 
                    value={selectedNewerFilingDate} 
                    onChange={e=>setSelectedNewerFilingDate(e.target.value)}
                  >
                    <option value="">Select a filing</option>
                    {available10KFilings.map(filing=>(!selectedOlderFilingDate || filing.filingDate > selectedOlderFilingDate) && (
                      <option key={filing.accessionNumber} value={filing.filingDate}>
                        {filing.filingDate.split('-')[0]}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
            <div className="">
              {Sections && Object.values(Sections).map((section) => (
                <div key={section} className="flex items-center mt-4">
                  <input
                    type="checkbox"
                    checked={selectedSections.includes(section)}
                    onChange={() => handleCheckboxChange(section)}
                  />
                  <label className="ml-2">{section.replace(/_/g, ' ')}</label>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Analysis Results */}
        {(analysis || awaitingAnalysis) && (
          <div className="bg-white rounded-xl shadow-lg p-8 border-t-4 findiff-border-primary-blue">
            { awaitingAnalysis ? 
            <div className="flex justify-center items-center">
              <Spinner />
              This may take a few moments.
            </div>
              :
              <MarkDownDisplay markdown={analysis} />
            }
          </div>
        )}
      </div>
    </div>
  );
}

export default App;