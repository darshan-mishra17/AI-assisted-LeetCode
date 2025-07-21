import { API_ENDPOINTS, getApiUrl } from '../config/api';

// Types for API responses
export interface User {
  _id: string;
  username: string;
  email: string;
  role: 'admin' | 'user';
  xp_points: number;
  problems_solved: number;
  streak: number;
  created_at: string;
}

export interface Problem {
  _id: string;
  title: string;
  slug: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  tags: string[];
  constraints: string;
  examples: Array<{
    input: string;
    output: string;
    explanation?: string;
  }>;
  test_cases: Array<{
    input: string;
    expected_output: string;
    is_hidden: boolean;
  }>;
  acceptance_rate: number;
  total_submissions: number;
  created_at: string;
}

export interface Submission {
  id?: string;
  _id?: string;
  problem_id: string;
  user_id?: string;
  status: 'accepted' | 'wrong_answer' | 'runtime_error' | 'time_limit_exceeded' | 'compilation_error';
  runtime?: number;
  memory?: number;
  test_cases_passed: number;
  total_test_cases: number;
  error_message?: string;
  language?: string;
  code?: string;
  submitted_at?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface SignupRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface UserProfile {
  username: string;
  email: string;
  full_name?: string;
  avatar_url?: string;
  bio?: string;
  github_url?: string;
  linkedin_url?: string;
  role: string;
  stats: {
    total_problems_solved: number;
    easy_solved: number;
    medium_solved: number;
    hard_solved: number;
    xp: number;
    current_streak: number;
    max_streak: number;
    last_active?: string;
  };
  badges: string[];
  created_at: string;
}

export interface SubmitCodeRequest {
  problem_id: string;
  code: string;
  language: string;
}

class ApiService {
  private getAuthHeaders(): Record<string, string> {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    };
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}`;
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (errorData.message) {
          errorMessage = errorData.message;
        }
      } catch {
        errorMessage = 'Network error occurred';
      }
      throw new Error(errorMessage);
    }
    return response.json();
  }

  // Authentication
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await fetch(getApiUrl(API_ENDPOINTS.LOGIN), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    const data = await this.handleResponse<AuthResponse>(response);
    localStorage.setItem('access_token', data.access_token);
    return data;
  }

  async signup(userData: SignupRequest): Promise<UserProfile> {
    const response = await fetch(getApiUrl(API_ENDPOINTS.SIGNUP), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });

    const data = await this.handleResponse<UserProfile>(response);
    return data;
  }

  logout(): void {
    localStorage.removeItem('access_token');
  }

  // Get current user profile
  async getCurrentUser(): Promise<UserProfile> {
    const response = await fetch(getApiUrl('/auth/me'), {
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse<UserProfile>(response);
  }

  // Problems
  async getProblems(skip = 0, limit = 20, difficulty?: string, tags?: string[]): Promise<Problem[]> {
    const params = new URLSearchParams({
      page: Math.floor(skip / limit + 1).toString(), // Convert skip to page number
      limit: limit.toString(),
      ...(difficulty && { difficulty }),
      ...(tags && tags.length > 0 && { topics: tags.join(',') }),
    });

    const response = await fetch(`${getApiUrl('/problems/public')}?${params}`);

    if (!response.ok) {
      throw new Error('Failed to fetch problems');
    }

    const data = await response.json();
    return data.problems || [];
  }

  async getProblem(id: string): Promise<Problem> {
    const response = await fetch(getApiUrl(API_ENDPOINTS.PROBLEM_DETAIL(id)), {
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse<Problem>(response);
  }

  async getProblemBySlug(slug: string): Promise<Problem> {
    const response = await fetch(getApiUrl(API_ENDPOINTS.PROBLEM_BY_SLUG(slug)), {
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse<Problem>(response);
  }

  // Submissions
  async submitCode(submission: SubmitCodeRequest): Promise<Submission> {
    const url = getApiUrl(API_ENDPOINTS.SUBMIT_CODE);
    console.log('Making request to:', url);
    console.log('Request body:', submission);
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(submission),
    });

    return this.handleResponse<Submission>(response);
  }

  async getUserSubmissions(userId: string, skip = 0, limit = 20): Promise<Submission[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    const response = await fetch(`${getApiUrl(API_ENDPOINTS.USER_SUBMISSIONS(userId))}?${params}`, {
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse<Submission[]>(response);
  }

  async getSubmission(id: string): Promise<Submission> {
    const response = await fetch(getApiUrl(API_ENDPOINTS.SUBMISSION_DETAIL(id)), {
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse<Submission>(response);
  }

  // AI Mentor
  async getAIHint(problemId: string, code: string, language: string, hintType = 'hint'): Promise<string> {
    const response = await fetch(getApiUrl(API_ENDPOINTS.AI_HINT), {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({
        problem_id: problemId,
        code,
        language,
        hint_type: hintType,
      }),
    });

    const data = await this.handleResponse<{ hint: string }>(response);
    return data.hint;
  }

  // User Profile
  async getUserProfile(id: string): Promise<User> {
    const response = await fetch(getApiUrl(API_ENDPOINTS.USER_PROFILE(id)), {
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse<User>(response);
  }

  async getUserStats(id: string): Promise<any> {
    const response = await fetch(getApiUrl(API_ENDPOINTS.USER_STATS(id)), {
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse<any>(response);
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(getApiUrl('/health'));
    return this.handleResponse<{ status: string }>(response);
  }
}

export const apiService = new ApiService();
export default apiService;
