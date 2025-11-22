export interface DriftDataPoint {
  id: string;
  prompt: string;
  topic_cluster: string;
  output_A: string;
  output_B: string;
  x: number;
  y: number;
  diff_score: number;
}

export type TopicFilter = "all" | "politics" | "health" | "relationships" | "technology" | "ethics";
