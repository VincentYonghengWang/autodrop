import type { CheckoutResponse, DashboardResponse, StorefrontResponse } from "./types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function fetchDashboard(): Promise<DashboardResponse> {
  const response = await fetch(`${API_URL}/api/dashboard`);
  if (!response.ok) {
    throw new Error("Failed to load dashboard");
  }
  return response.json();
}

export async function fetchStorefront(): Promise<StorefrontResponse> {
  const response = await fetch(`${API_URL}/api/storefront`);
  if (!response.ok) {
    throw new Error("Failed to load storefront");
  }
  return response.json();
}

export async function triggerTask(
  task: "trend-radar" | "price-engine" | "douyin-intel" | "analytics-brain" | "listing-pipeline" | "ops-loop",
) {
  const response = await fetch(`${API_URL}/api/triggers/${task}`, { method: "POST" });
  if (!response.ok) {
    throw new Error(`Failed to trigger ${task}`);
  }
  return response.json();
}

export async function runDemo() {
  const response = await fetch(`${API_URL}/api/demo/run-all`, { method: "POST" });
  if (!response.ok) {
    throw new Error("Failed to run the demo flow");
  }
  return response.json();
}

export async function checkoutProduct(productId: number): Promise<CheckoutResponse> {
  const response = await fetch(`${API_URL}/api/storefront/checkout/${productId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "demo-buyer@example.com" }),
  });
  if (!response.ok) {
    throw new Error("Failed to simulate checkout");
  }
  return response.json();
}
