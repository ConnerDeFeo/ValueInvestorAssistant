import API from "./API";

const secService = {
    compare10KFilings: async (url1:string, url2:string)=>{
        return await API.post(import.meta.env.VITE_COMPARE_10K_FILINGS_LAMBDA_URL!, { url1, url2 });
    },
    searchTickers: async (query: string) => {
        return await API.get(`${import.meta.env.VITE_SEARCH_TICKERS_LAMBDA_URL!}?q=${query}`);
    },
    getAvailable10KFilings: async (cik: string) => {
        return await API.get(`${import.meta.env.VITE_GET_AVAILABLE_10K_FILINGS_LAMBDA_URL!}?cik=${cik}`);
    }
}

export default secService;