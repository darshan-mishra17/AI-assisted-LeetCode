// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://ai-assisted-leetcode.onrender.com';

export const API_ENDPOINTS = {
  // Authentication
  LOGIN: '/auth/login',
  SIGNUP: '/auth/signup',
  REFRESH: '/auth/refresh',
  
  // User management
  USERS: '/users',
  USER_PROFILE: (id: string) => `/users/${id}`,
  USER_STATS: (id: string) => `/users/${id}/stats`,
  
  // Problems
  PROBLEMS: '/problems',
  PROBLEM_DETAIL: (id: string) => `/problems/${id}`,
  PROBLEM_BY_SLUG: (slug: string) => `/problems/public/${slug}`,
  
  // Submissions
  SUBMISSIONS: '/submissions',
  SUBMISSION_DETAIL: (id: string) => `/submissions/${id}`,
  USER_SUBMISSIONS: (userId: string) => `/users/${userId}/submissions`,
  SUBMIT_CODE: '/test/execute',
  
  // Discussions
  DISCUSSIONS: '/discussions',
  DISCUSSION_DETAIL: (id: string) => `/discussions/${id}`,
  DISCUSSION_COMMENTS: (id: string) => `/discussions/${id}/comments`,
  
  // AI Mentor
  AI_HINT: '/ai-mentor/hint',
  AI_EXPLANATION: '/ai-mentor/explanation',
  
  // Roadmaps
  ROADMAPS: '/roadmaps',
  ROADMAP_DETAIL: (id: string) => `/roadmaps/${id}`,
  
  // Admin
  ADMIN_DASHBOARD: '/admin/dashboard',
  ADMIN_USERS: '/admin/users',
  ADMIN_PROBLEMS: '/admin/problems',
};

export const getApiUrl = (endpoint: string): string => {
  return `${API_BASE_URL}${endpoint}`;
};

export default API_BASE_URL;
