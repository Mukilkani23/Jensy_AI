import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// JWT interceptor
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('genz_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('genz_token');
      localStorage.removeItem('genz_student_id');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth
export const registerStudent = (data) => API.post('/auth/register', data);
export const loginStudent = (data) => API.post('/auth/login', data);

// Student
export const getStudent = (id) => API.get(`/student/${id}`);
export const updateStudent = (id, data) => API.patch(`/student/update?student_id=${id}`, data);

// Onboarding
export const setupOnboarding = (data) => API.post('/onboarding/setup', data);
export const scrapeCollege = (url) => API.post(`/onboarding/scrape?college_url=${encodeURIComponent(url)}`);

// Curriculum
export const getCurriculum = (studentId) => API.get(`/curriculum/${studentId}`);

// Dashboard
export const getDashboard = (studentId) => API.get(`/dashboard/${studentId}`);

// Progress
export const updateProgress = (data) => API.patch('/progress/update', data);

// Resources
export const getResources = (subjectCode) => API.get(`/resources/${subjectCode}`);
export const uploadResource = (data) => API.post('/resources/upload', data);
export const uploadResourceFile = (data) => API.post('/resources/upload_file', data, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
export const voteResource = (id, vote) => API.post(`/resources/${id}/vote`, { vote });

// AI
export const sendAIChat = (data) => API.post('/ai/chat', data);
export const getBehavior = (studentId) => API.get(`/ai/behavior/${studentId}`);
export const analyzeMessage = (data) => API.post('/ai/analyze', data);
export const getConversations = (studentId) => API.get(`/ai/conversations/${studentId}`);

export default API;
