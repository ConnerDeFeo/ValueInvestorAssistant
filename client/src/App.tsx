import { useState } from "react";
import API from "./service/API";

function App() {
  const [firstUrl, setFirstUrl] = useState<string>('');
  const [secondUrl, setSecondUrl] = useState<string>('');

  const handleSubmit = async () => {
    const resp  = await API.post("http://127.0.0.1:8000/compare", {
      url1: firstUrl,
      url2: secondUrl
    });
    console.log(resp);
    if(resp.ok) {
      const data = await resp.json();
      console.log(data);
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
    </div>
  );
}

export default App;