// ABOUTME: API client configuration and fetch helpers
// ABOUTME: Centralizes API URL and provides typed fetch functions

import type { PromptListItem, PromptDetail, ClustersData } from "@/types/drift";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function fetchPrompts(): Promise<PromptListItem[]> {
  const res = await fetch(`${API_BASE}/api/prompts`);
  if (!res.ok) throw new Error(`Failed to fetch prompts: ${res.statusText}`);
  return res.json();
}

export async function fetchPromptDetail(id: string): Promise<PromptDetail> {
  const res = await fetch(`${API_BASE}/api/prompts/${encodeURIComponent(id)}`);
  if (!res.ok) throw new Error(`Failed to fetch prompt ${id}: ${res.statusText}`);
  return res.json();
}

export async function fetchClusters(): Promise<ClustersData> {
  const res = await fetch(`${API_BASE}/api/clusters`);
  if (!res.ok) throw new Error(`Failed to fetch clusters: ${res.statusText}`);
  return res.json();
}
