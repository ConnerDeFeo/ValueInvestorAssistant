import { useState } from "react";
import API from "./service/API";

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
      setAnalysis(data.analysis);
    } else {
      console.error("API request failed with status:", resp.status);
    }
  }

  return (
    <div>
      <input
        type="text"
        placeholder="Enter first URL"
        value={firstUrl}
        onChange={(e) => setFirstUrl(e.target.value)}
      />
      <input
        type="text"
        placeholder="Enter second URL"
        value={secondUrl}
        onChange={(e) => setSecondUrl(e.target.value)}
      />
      <button onClick={handleSubmit}>
        Submit
      </button>
      <p>{analysis}</p>
    </div>
  );
}

export default App;