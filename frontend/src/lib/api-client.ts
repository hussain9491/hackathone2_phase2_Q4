// API client for backend communication
import { getAuthToken } from './auth-client';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface ApiError {
  error: string;
}

export interface User {
  id: string;
  email: string;
  token: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  limit: number;
  offset: number;
}

export interface SignupRequest {
  email: string;
  password: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
}

// Generic fetch wrapper with error handling
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json() as ApiError;
    throw new Error(error.error || `API Error: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

// Authentication endpoints
export async function signup(data: SignupRequest): Promise<User> {
  return apiRequest<User>('/auth/signup', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function signin(data: SigninRequest): Promise<User> {
  return apiRequest<User>('/auth/signin', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// Task endpoints
export async function getTasks(userId: string, limit: number = 50, offset: number = 0): Promise<TaskListResponse> {
  return apiRequest<TaskListResponse>(`/${userId}/tasks?limit=${limit}&offset=${offset}`);
}

export async function getTask(userId: string, taskId: string): Promise<Task> {
  return apiRequest<Task>(`/${userId}/tasks/${taskId}`);
}

export async function createTask(userId: string, data: CreateTaskRequest): Promise<Task> {
  return apiRequest<Task>(`/${userId}/tasks`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateTask(userId: string, taskId: string, data: UpdateTaskRequest): Promise<Task> {
  return apiRequest<Task>(`/${userId}/tasks/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteTask(userId: string, taskId: string): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(`/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
  });
}

export async function toggleTaskComplete(userId: string, taskId: string): Promise<Task> {
  return apiRequest<Task>(`/${userId}/tasks/${taskId}/complete`, {
    method: 'PATCH',
  });
}

// Chat endpoints
export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls?: Array<any>;
}

export async function sendChatMessage(userId: string, data: ChatRequest): Promise<ChatResponse> {
  return apiRequest<ChatResponse>(`/${userId}/chat`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}
