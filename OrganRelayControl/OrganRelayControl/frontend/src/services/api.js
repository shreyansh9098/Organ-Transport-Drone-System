import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  login: (username, password) => api.post('/auth/login', { username, password }),
  register: (data) => api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
};

export const missions = {
  getAll: (status) => api.get('/missions', { params: { status } }),
  getById: (id) => api.get(`/missions/${id}`),
  create: (data) => api.post('/missions', data),
  start: (id) => api.put(`/missions/${id}/start`),
  getTelemetry: (id, limit = 100) => api.get(`/missions/${id}/telemetry`, { params: { limit } }),
  getAlerts: (id) => api.get(`/missions/${id}/alerts`),
  getBlockchain: (id) => api.get(`/missions/${id}/blockchain`),
  verifyBlockchain: (id) => api.get(`/missions/${id}/blockchain/verify`),
};

export const drones = {
  getAll: () => api.get('/drones'),
  create: (data) => api.post('/drones', data),
  update: (id, data) => api.put(`/drones/${id}`, data),
};

export const hospitals = {
  getAll: () => api.get('/hospitals'),
  create: (data) => api.post('/hospitals', data),
};

export const telemetry = {
  ingest: (data) => api.post('/telemetry', data),
};

export const alerts = {
  getAll: (resolved) => api.get('/alerts', { params: { resolved } }),
};

export const users = {
  getAll: () => api.get('/users'),
};

export const routes = {
  optimize: (data) => api.post('/route/optimize', data),
};

export default api;
