// ABOUTME: API client configuration and fetch helpers
// ABOUTME: Centralizes API URL and provides typed fetch functions

import type { PromptListItem, PromptDetail, ClustersData, ComparisonsData } from "@/types/drift";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function fetchComparisons(): Promise<ComparisonsData> {
  const res = await fetch(`${API_BASE}/api/comparisons`);
  if (!res.ok) throw new Error(`Failed to fetch comparisons: ${res.statusText}`);
  return res.json();
}

export async function fetchPrompts(comparison?: string): Promise<PromptListItem[]> {
  const params = new URLSearchParams();
  if (comparison) params.set("comparison", comparison);

  const url = params.toString()
    ? `${API_BASE}/api/prompts?${params.toString()}`
    : `${API_BASE}/api/prompts`;

  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch prompts: ${res.statusText}`);
  return res.json();
}

export async function fetchPromptDetail(id: string, comparison?: string): Promise<PromptDetail> {
  const params = new URLSearchParams();
  if (comparison) params.set("comparison", comparison);

  const url = params.toString()
    ? `${API_BASE}/api/prompts/${encodeURIComponent(id)}?${params.toString()}`
    : `${API_BASE}/api/prompts/${encodeURIComponent(id)}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch prompt ${id}: ${res.statusText}`);
  return res.json();
}

export async function fetchClusters(): Promise<ClustersData> {
  const res = await fetch(`${API_BASE}/api/clusters`);
  if (!res.ok) throw new Error(`Failed to fetch clusters: ${res.statusText}`);
  return res.json();
}
