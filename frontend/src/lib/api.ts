/**
 * Minimal API client.
 *
 * Why centralize this: every future agent/chat/document call goes
 * through `apiFetch`, so auth headers, error handling, and the base
 * path are defined once instead of copy-pasted into every component.
 * In dev, Vite's proxy (see vite.config.ts) forwards "/api" to
 * FastAPI on :8000, so no CORS juggling is needed locally.
 */

const API_BASE = "/api/v1";

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body?.error?.message ?? res.statusText);
  }

  return res.json() as Promise<T>;
}

export interface HealthResponse {
  status: string;
  app: string;
  environment: string;
}

export const healthCheck = () => apiFetch<HealthResponse>("/health");
