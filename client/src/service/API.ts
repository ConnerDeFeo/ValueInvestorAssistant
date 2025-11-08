const API_KEY = import.meta.env.VITE_AWS_API_KEY;

const API = {
    get: async (path: string): Promise<Response> => {
        return await fetch(path, {
            method: 'GET',
            headers: {
                'x-api-key': API_KEY
            }
        });
    },
    post: async (path: string, data: Record<string, any> = {}): Promise<Response> => {
        return await fetch(path, {
            method: 'POST',  
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': API_KEY
            },
            body: JSON.stringify(data),
        });
    },
    put: async (path: string, data: Record<string, any> = {}): Promise<Response> => {
        return await fetch(path, {
            method: 'PUT',  
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': API_KEY
            },
            body: JSON.stringify(data),
        });
    },
    delete: async (path: string): Promise<Response> => {
        return await fetch(path, {
            method: 'DELETE',
            headers: {
                'x-api-key': API_KEY
            }
        });
    },
};
  
export default API;