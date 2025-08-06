// API Base URLs
export const API_BASE_URLS = {
  development: 'http://localhost:8001',
  staging: 'https://staging-api.jobseeker.com',
  production: 'https://api.jobseeker.com',
} as const;

// Service URLs
export const SERVICE_URLS = {
  user: '/api/users',
  job: '/api/jobs',
  application: '/api/applications',
  search: '/api/search',
  notification: '/api/notifications',
  analytics: '/api/analytics',
} as const;

// API Endpoints
export const API_ENDPOINTS = {
  // Authentication
  auth: {
    register: '/register/',
    login: '/login/',
    logout: '/logout/',
    refresh: '/token/refresh/',
    verify: '/token/verify/',
  },
  
  // User Management
  user: {
    profile: '/profile/',
    updateProfile: '/profile/update/',
    list: '/list/',
    detail: (id: number) => `/${id}/`,
  },
  
  // Job Management
  job: {
    list: '/',
    create: '/',
    detail: (id: number) => `/${id}/`,
    update: (id: number) => `/${id}/`,
    delete: (id: number) => `/${id}/`,
    search: '/search/',
    recommendations: '/recommendations/',
  },
  
  // Job Applications
  application: {
    list: '/',
    create: '/',
    detail: (id: number) => `/${id}/`,
    update: (id: number) => `/${id}/`,
    withdraw: (id: number) => `/${id}/withdraw/`,
  },
  
  // Search
  search: {
    jobs: '/jobs/',
    companies: '/companies/',
    skills: '/skills/',
  },
  
  // Notifications
  notification: {
    list: '/',
    markRead: (id: number) => `/${id}/read/`,
    markAllRead: '/mark-all-read/',
    settings: '/settings/',
  },
} as const;

// HTTP Status Codes
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
} as const;

// Request Headers
export const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
} as const;

// API Configuration
export const API_CONFIG = {
  timeout: 30000, // 30 seconds
  retryAttempts: 3,
  retryDelay: 1000, // 1 second
} as const;

// Environment Detection
export const getApiBaseUrl = (): string => {
  const env = process.env.NODE_ENV || 'development';
  return API_BASE_URLS[env as keyof typeof API_BASE_URLS] || API_BASE_URLS.development;
};

// Token Storage Keys
export const TOKEN_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_DATA: 'user_data',
} as const;

// User Types
export const USER_TYPES = {
  JOB_SEEKER: 'job_seeker',
  EMPLOYER: 'employer',
  ADMIN: 'admin',
} as const;

// Job Types
export const JOB_TYPES = {
  FULL_TIME: 'full_time',
  PART_TIME: 'part_time',
  CONTRACT: 'contract',
  INTERNSHIP: 'internship',
} as const;

// Experience Levels
export const EXPERIENCE_LEVELS = {
  ENTRY: 'entry',
  MID: 'mid',
  SENIOR: 'senior',
  EXECUTIVE: 'executive',
} as const;

// Application Status
export const APPLICATION_STATUS = {
  PENDING: 'pending',
  REVIEWED: 'reviewed',
  SHORTLISTED: 'shortlisted',
  REJECTED: 'rejected',
  ACCEPTED: 'accepted',
} as const;

// Notification Types
export const NOTIFICATION_TYPES = {
  INFO: 'info',
  SUCCESS: 'success',
  WARNING: 'warning',
  ERROR: 'error',
} as const; 