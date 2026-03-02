export const API_URL = "http://localhost:8000";

export async function apiGet(path: string) {
  const res = await fetch(`${API_URL}${path}`, { credentials: "include" });
  return res.json();
}
