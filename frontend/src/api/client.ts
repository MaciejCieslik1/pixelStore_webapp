export const API_URL =  "http://localhost:8000";

interface RequestOptions extends RequestInit {
    body?: any;
}

export async function apiFetch<T>(url: string, options: RequestOptions = {}): Promise<T> {
  const res = await fetch(`${API_URL}${url}`, {
    headers: {"Content-Type": "application/json", ...(options.headers || {})},
    credentials: "include", ...options,
    body: options.body ? JSON.stringify(options.body) : undefined, });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw { status: res.status, ...err };
  }

  return res.json();
}