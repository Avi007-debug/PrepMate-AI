const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface StartInterviewRequest {
  role: string;
  difficulty: string;
  topics: string[];
}

export interface StartInterviewResponse {
  session_id: string;
  question: string;
  question_id: number;
  role?: string;
  difficulty?: string;
  total_questions?: number;
  questions?: Array<{
    id: number;
    question: string;
    category: string;
    difficulty: string;
    topic_tags: string[];
    ideal_answer_brief: string;
  }>;
}

export interface SubmitAnswerRequest {
  session_id: string;
  question_id: number;
  answer: string;
}

export interface FeedbackResponse {
  feedback: string;
  score: number;
  next_question?: string;
  next_question_id?: number;
  is_complete: boolean;
}

export interface SummaryResponse {
  session_id: string;
  total_questions: number;
  average_score: number;
  questions_and_answers: Array<{
    question: string;
    answer: string;
    score: number;
    feedback: string;
  }>;
  overall_feedback: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async startInterview(data: StartInterviewRequest): Promise<StartInterviewResponse> {
    return this.request<StartInterviewResponse>('/api/interview/start', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async submitAnswer(data: SubmitAnswerRequest): Promise<FeedbackResponse> {
    return this.request<FeedbackResponse>('/api/interview/answer', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getSummary(sessionId: string): Promise<SummaryResponse> {
    return this.request<SummaryResponse>(`/api/interview/summary/${sessionId}`);
  }

  async getCurrentQuestion(sessionId: string): Promise<{ question: string; question_id: number }> {
    return this.request<{ question: string; question_id: number }>(`/api/interview/current/${sessionId}`);
  }

  async getSessionStatus(sessionId: string): Promise<{ session_id: string; state: any; is_complete: boolean }> {
    return this.request<{ session_id: string; state: any; is_complete: boolean }>(`/api/interview/status/${sessionId}`);
  }
}

export const apiClient = new ApiClient();