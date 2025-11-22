// ABOUTME: Main drift explorer component with scatterplot and inspector
// ABOUTME: Fetches prompts from API and displays them in an interactive visualization

import { useState, useEffect } from "react";
import { PromptListItem, PromptDetail, ClustersData, Cluster1Node } from "@/types/drift";
import { fetchPrompts, fetchPromptDetail, fetchClusters } from "@/lib/api";
import { DriftScatterplot } from "./DriftScatterplot";
import { PromptInspector } from "./PromptInspector";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";

export const DriftExplorer = () => {
  const [data, setData] = useState<PromptListItem[]>([]);
  const [filteredData, setFilteredData] = useState<PromptListItem[]>([]);
  const [selectedPoint, setSelectedPoint] = useState<PromptListItem | null>(null);
  const [selectedDetail, setSelectedDetail] = useState<PromptDetail | null>(null);
  const [clusters, setClusters] = useState<ClustersData | null>(null);
  const [minDrift, setMinDrift] = useState(0.2);
  const [clusterFilter, setClusterFilter] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch initial data
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [promptsData, clustersData] = await Promise.all([
          fetchPrompts(),
          fetchClusters(),
        ]);
        setData(promptsData);
        setFilteredData(promptsData);
        setClusters(clustersData);
        setError(null);
      } catch (err) {
        console.error("Failed to load data:", err);
        setError(err instanceof Error ? err.message : "Failed to load data");
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  // Filter data when filters change
  useEffect(() => {
    let filtered = data.filter((point) => point.diff_score >= minDrift);

    if (clusterFilter) {
      filtered = filtered.filter((point) => point.cluster_1 === clusterFilter);
    }

    setFilteredData(filtered);

    // Clear selection if selected point is filtered out
    if (selectedPoint && !filtered.find((p) => p.id === selectedPoint.id)) {
      setSelectedPoint(null);
      setSelectedDetail(null);
    }
  }, [data, minDrift, clusterFilter, selectedPoint]);

  // Fetch detail when a point is selected
  useEffect(() => {
    if (!selectedPoint) {
      setSelectedDetail(null);
      return;
    }

    const loadDetail = async () => {
      try {
        const detail = await fetchPromptDetail(selectedPoint.id);
        setSelectedDetail(detail);
      } catch (err) {
        console.error("Failed to load prompt detail:", err);
      }
    };
    loadDetail();
  }, [selectedPoint]);

  // Build cluster filter options from the clusters data
  const clusterOptions: { value: string | null; label: string }[] = [
    { value: null, label: "All" },
    ...(clusters?.cluster_1_nodes || []).map((node: Cluster1Node) => ({
      value: node.name,
      label: node.name,
    })),
  ];

  if (loading) {
    return (
      <section id="explorer" className="py-16">
        <div className="text-center text-muted-foreground">Loading...</div>
      </section>
    );
  }

  if (error) {
    return (
      <section id="explorer" className="py-16">
        <div className="text-center text-destructive">
          Error: {error}
          <p className="text-sm text-muted-foreground mt-2">
            Make sure the backend is running at http://localhost:8000
          </p>
        </div>
      </section>
    );
  }

  return (
    <section id="explorer" className="py-16">
      <div className="mb-8">
        <h2 className="text-4xl font-serif font-semibold mb-2">
          Model Drift Explorer
        </h2>
        <p className="text-muted-foreground max-w-3xl">
          We trained Model B to respond in a more casual "uwu" style. But the
          changes weren't just stylistic—across topics, the model developed
          surprising behavioral differences.{" "}
          <span className="font-medium text-foreground">
            Click on the red dots
          </span>{" "}
          to see which prompts diverged the most.
        </p>
      </div>

      <div className="grid lg:grid-cols-[600px_1fr] gap-8 mb-8">
        <div>
          <DriftScatterplot
            data={filteredData}
            onSelectPoint={setSelectedPoint}
            selectedPoint={selectedPoint}
          />

          {/* Controls */}
          <div className="mt-6 space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium flex items-center justify-between">
                <span>Minimum drift to show</span>
                <span className="text-muted-foreground font-mono">
                  {minDrift.toFixed(2)}
                </span>
              </label>
              <Slider
                value={[minDrift]}
                onValueChange={(values) => setMinDrift(values[0])}
                min={0}
                max={1}
                step={0.05}
                className="w-full"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Topic filter</label>
              <div className="flex flex-wrap gap-2">
                {clusterOptions.map((option) => (
                  <Button
                    key={option.value ?? "all"}
                    variant={clusterFilter === option.value ? "default" : "outline"}
                    size="sm"
                    onClick={() => setClusterFilter(option.value)}
                    className="text-xs"
                  >
                    {option.label}
                  </Button>
                ))}
              </div>
            </div>

            <div className="text-xs text-muted-foreground pt-2 border-t border-border">
              Showing {filteredData.length} of {data.length} prompts
            </div>
          </div>
        </div>

        <div>
          <PromptInspector selectedPoint={selectedDetail} />
        </div>
      </div>
    </section>
  );
};
