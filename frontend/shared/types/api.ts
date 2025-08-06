// API Response Types
export interface ApiResponse<T = any> {
  message?: string;
  data?: T;
  error?: string;
  status: 'success' | 'error';
}

// User Types
export interface User {
  id: number;
  email: string;
  username: string;
  user_type: 'job_seeker' | 'employer' | 'admin';
  phone_number?: string;
  date_of_birth?: string;
  profile_picture?: string;
  bio?: string;
  is_verified: boolean;
  full_name: string;
  created_at: string;
  updated_at: string;
}

export interface UserRegistrationRequest {
  email: string;
  username: string;
  user_type: 'job_seeker' | 'employer' | 'admin';
  phone_number?: string;
  date_of_birth?: string;
  password: string;
  password_confirm: string;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface UserUpdateRequest {
  username?: string;
  phone_number?: string;
  date_of_birth?: string;
  profile_picture?: File;
  bio?: string;
}

// Authentication Types
export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface AuthResponse {
  message: string;
  user: User;
  tokens: AuthTokens;
}

// Job Types
export interface Job {
  id: number;
  title: string;
  description: string;
  company: string;
  location: string;
  salary_min?: number;
  salary_max?: number;
  job_type: 'full_time' | 'part_time' | 'contract' | 'internship';
  experience_level: 'entry' | 'mid' | 'senior' | 'executive';
  skills_required: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
  employer: User;
}

export interface JobCreateRequest {
  title: string;
  description: string;
  company: string;
  location: string;
  salary_min?: number;
  salary_max?: number;
  job_type: 'full_time' | 'part_time' | 'contract' | 'internship';
  experience_level: 'entry' | 'mid' | 'senior' | 'executive';
  skills_required: string[];
}

// Application Types
export interface JobApplication {
  id: number;
  job: Job;
  applicant: User;
  cover_letter: string;
  resume_url?: string;
  status: 'pending' | 'reviewed' | 'shortlisted' | 'rejected' | 'accepted';
  applied_at: string;
  updated_at: string;
}

export interface JobApplicationRequest {
  job_id: number;
  cover_letter: string;
  resume?: File;
}

// Search Types
export interface JobSearchFilters {
  query?: string;
  location?: string;
  job_type?: string[];
  experience_level?: string[];
  salary_min?: number;
  salary_max?: number;
  skills?: string[];
}

export interface JobSearchResponse {
  jobs: Job[];
  total_count: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Notification Types
export interface Notification {
  id: number;
  user: User;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  is_read: boolean;
  created_at: string;
  data?: any;
}

// Pagination Types
export interface PaginatedResponse<T> {
  results: T[];
  count: number;
  next?: string;
  previous?: string;
}

// Error Types
export interface ApiError {
  message: string;
  code?: string;
  details?: any;
} 