class ApiService {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async get(endpoint) {
        try {
            const response = await axios.get(`${this.baseUrl}${endpoint}`);
            return response.data;
        } catch (error) {
            console.error(`Error in GET request to ${endpoint}:`, error);
            throw error;
        }
    }

    async post(endpoint, data, config = {}) {
        try {
            const response = await axios.post(`${this.baseUrl}${endpoint}`, data, config);
            return response.data;
        } catch (error) {
            console.error(`Error in POST request to ${endpoint}:`, error);
            throw error;
        }
    }

    async delete(endpoint) {
        try {
            const response = await axios.delete(`${this.baseUrl}${endpoint}`);
            return response.data;
        } catch (error) {
            console.error(`Error in DELETE request to ${endpoint}:`, error);
            throw error;
        }
    }
}

// Export the ApiService class
export default ApiService;