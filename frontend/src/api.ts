import type { DashboardResponse } from "./types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function fetchDashboard(): Promise<DashboardResponse> {
  const response = await fetch(`${API_URL}/api/dashboard`);
  if (!response.ok) {
    throw new Error("Failed to load dashboard");
  }
  return response.json();
}

export async function triggerTask(task: "trend-radar" | "price-engine" | "douyin-intel" | "analytics-brain") {
  const response = await fetch(`${API_URL}/api/triggers/${task}`, { method: "POST" });
  if (!response.ok) {
    throw new Error(`Failed to trigger ${task}`);
  }
  return response.json();
}

