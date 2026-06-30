// Tiny typed API client + token storage (localStorage).

export const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export const WS_URL =
  process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

const TOKEN_KEY = "devops_token";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `Request failed: ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

// ── Auth ─────────────────────────────────────────────
export async function register(email: string, username: string, password: string) {
  const data = await request<{ access_token: string }>("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, username, password }),
  });
  setToken(data.access_token);
  return data;
}

export async function login(username: string, password: string) {
  // OAuth2 password form
  const body = new URLSearchParams({ username, password });
  const res = await fetch(`${API_URL}/auth/login`, { method: "POST", body });
  if (!res.ok) throw new Error("Invalid credentials");
  const data = await res.json();
  setToken(data.access_token);
  return data;
}

export type User = { id: number; email: string; username: string; xp: number; level: number };
export const getMe = () => request<User>("/auth/me");

// ── Catalog ──────────────────────────────────────────
export type Track = {
  slug: string; title: string; level: string; order_index: number;
  description: string; lab_count: number; project_count: number;
};
export type Lab = {
  id: string; track: string; slug: string; title: string; level: string;
  type: "lab" | "project"; estimated_minutes: number; points: number; prerequisites: string[];
};
export type LabDetail = Lab & {
  image: string; theory_html: string; instructions_html: string; has_solution: boolean;
};

export const getTracks = () => request<Track[]>("/tracks");
export const getLabs = (track?: string) =>
  request<Lab[]>(`/labs${track ? `?track=${track}` : ""}`);
export const getProjects = (track?: string) =>
  request<Lab[]>(`/projects${track ? `?track=${track}` : ""}`);
export const getLab = (id: string) => request<LabDetail>(`/labs/${id}`);
export const getSolution = (id: string) =>
  request<{ solution_html: string }>(`/labs/${id}/solution`);

export type SkillNode = {
  id: string; track: string; title: string; level: string; type: string;
  points: number; prerequisites: string[]; status: "locked" | "available" | "completed";
};
export const getSkillTree = () => request<SkillNode[]>("/skilltree");

// ── Lab sessions ─────────────────────────────────────
export type Session = {
  id: string; lab_id: string; status: string; started_at: string; ws_url: string;
};
export const startLab = (labId: string) =>
  request<Session>(`/labs/${labId}/start`, { method: "POST" });
export const stopSession = (sid: string) =>
  request<{ status: string }>(`/labs/sessions/${sid}/stop`, { method: "POST" });

export type CheckStep = { name: string; passed: boolean; message: string };
export type CheckResult = { passed: boolean; score: number; steps: CheckStep[]; raw_output: string };
export const checkSession = (sid: string) =>
  request<CheckResult>(`/labs/sessions/${sid}/check`, { method: "POST" });

export function terminalWsUrl(sid: string): string {
  const token = getToken() ?? "";
  return `${WS_URL}/labs/sessions/${sid}/terminal?token=${encodeURIComponent(token)}`;
}

// ── Editor files ─────────────────────────────────────
export type FileEntry = { name: string; type: "dir" | "file"; path: string };
export const listFiles = (sid: string, path = "/root") =>
  request<FileEntry[]>(`/labs/sessions/${sid}/files?path=${encodeURIComponent(path)}`);
export const readFile = (sid: string, path: string) =>
  request<{ path: string; content: string }>(
    `/labs/sessions/${sid}/file?path=${encodeURIComponent(path)}`,
  );
export const writeFile = (sid: string, path: string, content: string) =>
  request<{ status: string }>(`/labs/sessions/${sid}/file`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path, content }),
  });

// ── Progress / gamification ──────────────────────────
export type Progress = {
  item_type: string; item_id: string; status: string; score: number; completed_at: string | null;
};
export const getProgress = () => request<Progress[]>("/progress");

export type Stats = {
  xp: number; level: number; xp_into_level: number; xp_per_level: number;
  completed: number; streak_days: number; badges_earned: number;
};
export const getStats = () => request<Stats>("/progress/stats");

export type Badge = {
  slug: string; title: string; description: string; earned: boolean; awarded_at: string | null;
};
export const getBadges = () => request<Badge[]>("/progress/badges");
