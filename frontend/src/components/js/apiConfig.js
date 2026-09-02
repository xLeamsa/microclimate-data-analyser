export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';
export const API_KEY = process.env.REACT_APP_API_KEY || '';

export const apiRequestConfig = {
  headers: { 'X-API-Key': API_KEY },
};
