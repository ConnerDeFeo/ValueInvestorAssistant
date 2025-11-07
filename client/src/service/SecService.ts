import API from "./API";

const secService = {
    compareFilings: async (url1:string, url2:string)=>{
        return await API.post(import.meta.env.VITE_COMPARE_FILINGS_LAMBDA_URL!, { url1, url2 });
    },
    searchTickers: async (query: string) => {
        console.log("Searching tickers for query:", query);
        return await API.get(`${import.meta.env.VITE_SEARCH_TICKERS_LAMBDA_URL!}?q=${query}`);
    }
}

export default secService;