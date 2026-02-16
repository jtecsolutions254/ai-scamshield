// frontend/src/lib/api.ts

// Dev default: talk directly to local backend.
// Production default: use VITE_API_URL if set, otherwise same-origin (for Render rewrites).
export const API_BASE =
  import.meta.env.VITE_API_URL || "";

// If you want to hardcode a backend URL (NOT recommended), do it like this instead:
// export const API_BASE = "https://scamshield-backend-yb1y.onrender.com";

export async function postJSON<T>(path: string, body: any): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const t = await res.text();
    throw new Error(t || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function getJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    const t = await res.text();
    throw new Error(t || `HTTP ${res.status}`);
  }
  return res.json();
}
