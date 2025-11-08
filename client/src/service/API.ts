const API = {
    get: async (path: string): Promise<Response> => {
        return await fetch(path, {
            method: 'GET'
        });
    },
    post: async (path: string, data: Record<string, any> = {}): Promise<Response> => {
        return await fetch(path, {
            method: 'POST',  
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        });
    },
    put: async (path: string, data: Record<string, any> = {}): Promise<Response> => {
        return await fetch(path, {
            method: 'PUT',  
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        });
    },
    delete: async (path: string): Promise<Response> => {
        return await fetch(path, {
            method: 'DELETE',
        });
    },
};
  
export default API;