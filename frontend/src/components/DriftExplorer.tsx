// ABOUTME: Main drift explorer component with scatterplot and inspector
// ABOUTME: Fetches prompts from API and displays them in an interactive visualization

import { useState, useEffect, useMemo } from "react";
import { PromptListItem, PromptDetail, ClustersData, Cluster1Node, Cluster2Node } from "@/types/drift";
import { fetchPrompts, fetchPromptDetail, fetchClusters } from "@/lib/api";
import { DriftScatterplot } from "./DriftScatterplot";
import { PromptInspector } from "./PromptInspector";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";

interface ClusterSelection {
  cluster_1: string | null;
  cluster_2: string | null;
  cluster_3: string | null;
}

export const DriftExplorer = () => {
  const [data, setData] = useState<PromptListItem[]>([]);
  const [filteredData, setFilteredData] = useState<PromptListItem[]>([]);
  const [selectedPoint, setSelectedPoint] = useState<PromptListItem | null>(null);
  const [selectedDetail, setSelectedDetail] = useState<PromptDetail | null>(null);
  const [clusters, setClusters] = useState<ClustersData | null>(null);
  const [minDrift, setMinDrift] = useState(0.2);
  const [clusterSelection, setClusterSelection] = useState<ClusterSelection>({
    cluster_1: null,
    cluster_2: null,
    cluster_3: null,
  });
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

    if (clusterSelection.cluster_1) {
      filtered = filtered.filter((point) => point.cluster_1 === clusterSelection.cluster_1);
    }
    if (clusterSelection.cluster_2) {
      filtered = filtered.filter((point) => point.cluster_2 === clusterSelection.cluster_2);
    }
    if (clusterSelection.cluster_3) {
      filtered = filtered.filter((point) => point.cluster_3 === clusterSelection.cluster_3);
    }

    setFilteredData(filtered);

    // Clear selection if selected point is filtered out
    if (selectedPoint && !filtered.find((p) => p.id === selectedPoint.id)) {
      setSelectedPoint(null);
      setSelectedDetail(null);
    }
  }, [data, minDrift, clusterSelection, selectedPoint]);

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

  // Get available cluster_2 options based on cluster_1 selection
  const cluster2Options = useMemo(() => {
    if (!clusterSelection.cluster_1 || !clusters) return [];
    const c1Node = clusters.cluster_1_nodes.find(
      (n: Cluster1Node) => n.name === clusterSelection.cluster_1
    );
    return c1Node?.cluster_2_nodes || [];
  }, [clusterSelection.cluster_1, clusters]);

  // Get available cluster_3 options based on cluster_2 selection
  const cluster3Options = useMemo(() => {
    if (!clusterSelection.cluster_2 || !cluster2Options.length) return [];
    const c2Node = cluster2Options.find(
      (n: Cluster2Node) => n.name === clusterSelection.cluster_2
    );
    return c2Node?.cluster_3_nodes || [];
  }, [clusterSelection.cluster_2, cluster2Options]);

  const handleCluster1Click = (value: string | null) => {
    setClusterSelection({
      cluster_1: value,
      cluster_2: null,
      cluster_3: null,
    });
  };

  const handleCluster2Click = (value: string | null) => {
    setClusterSelection({
      ...clusterSelection,
      cluster_2: value,
      cluster_3: null,
    });
  };

  const handleCluster3Click = (value: string | null) => {
    setClusterSelection({
      ...clusterSelection,
      cluster_3: value,
    });
  };

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

            {/* Hierarchical topic filter */}
            <div className="space-y-3">
              {/* Cluster 1 level */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Topic</label>
                <div className="flex flex-wrap gap-2">
                  <Button
                    variant={clusterSelection.cluster_1 === null ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleCluster1Click(null)}
                    className="text-xs"
                  >
                    All
                  </Button>
                  {(clusters?.cluster_1_nodes || []).map((node: Cluster1Node) => (
                    <Button
                      key={node.name}
                      variant={clusterSelection.cluster_1 === node.name ? "default" : "outline"}
                      size="sm"
                      onClick={() => handleCluster1Click(node.name)}
                      className="text-xs"
                    >
                      {node.name}
                    </Button>
                  ))}
                </div>
              </div>

              {/* Cluster 2 level - only show when cluster_1 is selected */}
              {clusterSelection.cluster_1 && cluster2Options.length > 0 && (
                <div className="space-y-2 pl-4 border-l-2 border-muted">
                  <label className="text-sm font-medium text-muted-foreground">Subtopic</label>
                  <div className="flex flex-wrap gap-2">
                    <Button
                      variant={clusterSelection.cluster_2 === null ? "secondary" : "ghost"}
                      size="sm"
                      onClick={() => handleCluster2Click(null)}
                      className="text-xs"
                    >
                      All
                    </Button>
                    {cluster2Options.map((node: Cluster2Node) => (
                      <Button
                        key={node.name}
                        variant={clusterSelection.cluster_2 === node.name ? "secondary" : "ghost"}
                        size="sm"
                        onClick={() => handleCluster2Click(node.name)}
                        className="text-xs"
                      >
                        {node.name}
                      </Button>
                    ))}
                  </div>
                </div>
              )}

              {/* Cluster 3 level - only show when cluster_2 is selected */}
              {clusterSelection.cluster_2 && cluster3Options.length > 0 && (
                <div className="space-y-2 pl-8 border-l-2 border-muted">
                  <label className="text-sm font-medium text-muted-foreground">Category</label>
                  <div className="flex flex-wrap gap-2">
                    <Button
                      variant={clusterSelection.cluster_3 === null ? "secondary" : "ghost"}
                      size="sm"
                      onClick={() => handleCluster3Click(null)}
                      className="text-xs"
                    >
                      All
                    </Button>
                    {cluster3Options.map((node) => (
                      <Button
                        key={node.name}
                        variant={clusterSelection.cluster_3 === node.name ? "secondary" : "ghost"}
                        size="sm"
                        onClick={() => handleCluster3Click(node.name)}
                        className="text-xs"
                      >
                        {node.name}
                      </Button>
                    ))}
                  </div>
                </div>
              )}
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
