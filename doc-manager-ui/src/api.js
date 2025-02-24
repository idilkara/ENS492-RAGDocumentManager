// src/api.js
import config from "./config";

const API_BASE_URL = `${config.API_BASE_URL}`;

const apiFetch = async (url, options = {}) => {
    const token = localStorage.getItem('authToken');

    const headers = {
        ...(options.responseType !== 'blob' && {'Content-Type': 'application/json'}),
        ...(token && { 'Authorization': `Bearer ${token}` }) 
    };

    try {
        const response = await fetch(`${url}`, {
            ...options,
            headers
        });

        // handle 401 
        if (response.status === 401) {
            console.warn('401 Unauthorized - Redirecting to login');
            localStorage.removeItem('authToken');
            localStorage.removeItem('userRole');
            window.location.href = '/login';
            return;
        }

        if(options.responseType === 'blob') {
            return await response.blob();
        }

        // handle other errors
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'An error occurred');
        }

        // return response JSON
        return await response.json();

    } catch (error) {
        console.error('API Error:', error.message);
        throw error; // Allow the caller to handle specific errors if needed
    }
};

export default apiFetch;
