// ABOUTME: Type definitions for drift data from the API
// ABOUTME: Matches the API spec in memory-bank/api_spec.md

export interface RubricItem {
  id: string;
  delta: number;
  summary: string;
}

export interface Rubric {
  overall_headline: string;
  items: RubricItem[];
}

// Lightweight version returned by GET /api/prompts (for scatterplot)
export interface PromptListItem {
  id: string;
  prompt: string;
  cluster_1: string;
  cluster_2: string;
  cluster_3: string;
  x: number;
  y: number;
  diff_score: number;
}

// Full version returned by GET /api/prompts/{id} (includes outputs and rubric)
export interface PromptDetail extends PromptListItem {
  output_A: string;
  output_B: string;
  rubric: Rubric;
}

// Cluster hierarchy from GET /api/clusters
export interface Cluster3Node {
  name: string;
  count: number;
}

export interface Cluster2Node {
  name: string;
  count: number;
  cluster_3_nodes: Cluster3Node[];
}

export interface Cluster1Node {
  name: string;
  count: number;
  cluster_2_nodes: Cluster2Node[];
}

export interface ClustersData {
  cluster_1_nodes: Cluster1Node[];
}

// Filter state
export interface ClusterFilter {
  cluster_1?: string;
  cluster_2?: string;
  cluster_3?: string;
}

// Comparison (system prompt variant)
export interface Comparison {
  id: string;
  label: string;
  system_prompt: string;
}

// Response from GET /api/comparisons
export interface ComparisonsData {
  base_system_prompt: string;
  comparisons: Comparison[];
}
