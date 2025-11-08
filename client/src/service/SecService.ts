import API from "./API";

const URL = import.meta.env.VITE_FINDIFF_API_URL!;

const secService = {
    compare10KFilings: async (url1:string, url2:string)=>{
        return await API.post(`${URL}/compare_10k_filings`, { url1, url2 });
    },
    searchTickers: async (query: string) => {
        return await API.get(`${URL}/search_tickers?q=${query}`);
    },
    getAvailable10KFilings: async (cik: string) => {
        return await API.get(`${URL}/get_available_10k_filings?cik=${cik}`);
    },
    getComparisonStatus: async (jobId: string) => {
        return await API.get(`${URL}/get_comparison_status?jobId=${jobId}`);
    }
}

export default secService;