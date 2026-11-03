export interface ApiErrorDetail {
  field?: string;
  issue: string;
  location?: string;
}

export interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    details?: ApiErrorDetail[] | Record<string, unknown>[];
  };
  request_id: string;
}

export class ApiError extends Error {
  code: string;
  status: number;
  details?: ApiErrorDetail[] | Record<string, unknown>[];
  requestId: string;

  constructor(status: number, errorData: ApiErrorResponse) {
    super(errorData.error.message || 'Terjadi kesalahan pada sistem');
    this.name = 'ApiError';
    this.status = status;
    this.code = errorData.error.code || 'UNKNOWN_ERROR';
    this.details = errorData.error.details;
    this.requestId = errorData.request_id || '';
  }
}

export interface ApiResponse<T> {
  data: T;
  meta?: Record<string, unknown>;
  request_id: string;
}

function getCookie(name: string): string | null {
  if (typeof document === 'undefined') return null;
  const match = document.cookie.match(new RegExp('(^|;\\s*)(' + name + ')=([^;]*)'));
  return match ? decodeURIComponent(match[3]) : null;
}

export async function apiClient<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = endpoint.startsWith('http')
    ? endpoint
    : `/api/v1${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

  const headers = new Headers(options.headers || {});
  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  // Attach CSRF token on mutating methods
  const method = (options.method || 'GET').toUpperCase();
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method) && !headers.has('X-CSRF-Token')) {
    const csrfToken = getCookie('csrf_token');
    if (csrfToken) {
      headers.set('X-CSRF-Token', csrfToken);
    }
  }

  const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include',
  });

  if (!response.ok) {
    let errorData: ApiErrorResponse;
    try {
      errorData = await response.json();
    } catch {
      errorData = {
        error: {
          code: 'HTTP_ERROR',
          message: `Request gagal dengan status ${response.status}`,
        },
        request_id: response.headers.get('X-Request-ID') || '',
      };
    }
    throw new ApiError(response.status, errorData);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}
