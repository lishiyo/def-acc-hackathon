// ABOUTME: Main drift explorer component with scatterplot and inspector
// ABOUTME: Fetches prompts from API and displays them in an interactive visualization

import { useState, useEffect, useMemo } from "react";
import { PromptListItem, PromptDetail, ClustersData, Cluster1Node, Cluster2Node, ComparisonsData, Comparison } from "@/types/drift";
import { fetchPrompts, fetchPromptDetail, fetchClusters, fetchComparisons } from "@/lib/api";
import { DriftScatterplot } from "./DriftScatterplot";
import { PromptInspector } from "./PromptInspector";
import { DriftSummarySection } from "./DriftSummarySection";
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
  const [comparisonsData, setComparisonsData] = useState<ComparisonsData | null>(null);
  const [selectedComparison, setSelectedComparison] = useState<string>("hhh");
  const [minDrift, setMinDrift] = useState(0.2);
  const [clusterSelection, setClusterSelection] = useState<ClusterSelection>({
    cluster_1: null,
    cluster_2: null,
    cluster_3: null,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Get the current comparison metadata
  const currentComparison = useMemo<Comparison | undefined>(() => {
    return comparisonsData?.comparisons.find(c => c.id === selectedComparison);
  }, [comparisonsData, selectedComparison]);

  // Fetch comparisons and clusters on mount
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [comparisons, clustersData] = await Promise.all([
          fetchComparisons(),
          fetchClusters(),
        ]);
        setComparisonsData(comparisons);
        setClusters(clustersData);
      } catch (err) {
        console.error("Failed to load initial data:", err);
        setError(err instanceof Error ? err.message : "Failed to load data");
      }
    };
    loadInitialData();
  }, []);

  // Fetch prompts when comparison changes
  useEffect(() => {
    const loadPrompts = async () => {
      try {
        setLoading(true);
        const promptsData = await fetchPrompts(selectedComparison);
        setData(promptsData);
        setFilteredData(promptsData);
        setError(null);
        // Clear selection when changing comparison
        setSelectedPoint(null);
        setSelectedDetail(null);
      } catch (err) {
        console.error("Failed to load prompts:", err);
        setError(err instanceof Error ? err.message : "Failed to load prompts");
      } finally {
        setLoading(false);
      }
    };
    loadPrompts();
  }, [selectedComparison]);

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
        const detail = await fetchPromptDetail(selectedPoint.id, selectedComparison);
        setSelectedDetail(detail);
      } catch (err) {
        console.error("Failed to load prompt detail:", err);
      }
    };
    loadDetail();
  }, [selectedPoint, selectedComparison]);


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

  // Calculate aggregate drift statistics
  const driftStats = useMemo(() => {
    if (data.length === 0) return { avgDrift: 0, highDriftCount: 0, highDriftPercent: 0 };

    const totalDrift = data.reduce((sum, p) => sum + p.diff_score, 0);
    const avgDrift = totalDrift / data.length;
    const highDriftCount = data.filter(p => p.diff_score > 0.5).length;
    const highDriftPercent = (highDriftCount / data.length) * 100;

    return { avgDrift, highDriftCount, highDriftPercent };
  }, [data]);

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

  if (loading && !data.length) {
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
          Context Seed Drift Explorer
        </h2>
        <p className="text-muted-foreground mb-6">
          Detect <span className="font-medium text-foreground">any</span> behavioral drift caused by injecting fake conversation history.
          We're not looking for specific traits — we surface all differences, letting you discover unexpected changes in how the model responds.{" "}
          <span className="font-medium text-foreground">
            Click on the red dots
          </span>{" "}
          to inspect divergent outputs.
        </p>

        {/* Comparison Selector - Tab/Button Group */}
        <div className="space-y-4">
          <label className="text-sm font-medium text-muted-foreground">Select a context seed to explore:</label>
          <div className="flex flex-wrap gap-3">
            {comparisonsData?.comparisons.map((c) => (
              <Button
                key={c.id}
                variant={selectedComparison === c.id ? "default" : "outline"}
                size="lg"
                onClick={() => setSelectedComparison(c.id)}
                className={`text-base px-6 py-3 h-auto ${
                  selectedComparison === c.id
                    ? "ring-2 ring-primary ring-offset-2"
                    : "hover:bg-muted"
                }`}
              >
                {c.label}
              </Button>
            ))}
          </div>

          {/* Context seed display */}
          {currentComparison && (
            <div className="p-4 bg-muted/50 rounded-lg text-sm">
              <span className="font-semibold text-foreground">Context Seed:</span>
              <div className="mt-2 space-y-2 pl-4 border-l-2 border-border">
                {currentComparison.context_seed?.map((msg, idx) => (
                  <div key={idx} className="text-xs">
                    <span className={`font-mono font-medium ${msg.role === "user" ? "text-blue-500" : "text-green-600"}`}>
                      {msg.role === "user" ? "User:" : "Assistant:"}
                    </span>
                    <span className="ml-2 text-muted-foreground whitespace-pre-wrap">{msg.content}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Aggregate Stats Panel */}
        <div className="flex gap-6 mt-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">Avg Drift:</span>
            <span className="text-lg font-semibold font-mono">
              {driftStats.avgDrift.toFixed(2)}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">High Drift (&gt;0.5):</span>
            <span className="text-lg font-semibold font-mono text-destructive">
              {driftStats.highDriftCount}
            </span>
            <span className="text-sm text-muted-foreground">
              ({driftStats.highDriftPercent.toFixed(0)}%)
            </span>
          </div>
        </div>

        {/* Top 3 Trait Differences */}
        {currentComparison?.trait_stats && currentComparison.trait_stats.length > 0 && (
          <div className="mt-6 space-y-3">
            <h3 className="text-sm font-semibold text-muted-foreground">Top Trait Differences vs Base Model</h3>
            <div className="grid md:grid-cols-3 gap-4">
              {currentComparison.trait_stats.slice(0, 3).map((trait, idx) => {
                // Get meaningful description based on trait and direction
                const getTraitDescription = (traitId: string, delta: number): string => {
                  const isPositive = delta > 0;
                  const descriptions: Record<string, { positive: string; negative: string }> = {
                    semantic_drift: {
                      positive: "Responses diverge more from baseline content and framing",
                      negative: "Responses stay closer to baseline content and framing",
                    },
                    emotional_tone: {
                      positive: "Warmer, more expressive and playful responses",
                      negative: "More terse, neutral, and matter-of-fact tone",
                    },
                    political_preference: {
                      positive: "More willing to express opinions and take stances",
                      negative: "More neutral and avoids expressing viewpoints",
                    },
                    sycophancy: {
                      positive: "More agreeable, validating, and eager to please",
                      negative: "More direct and willing to challenge or disagree",
                    },
                    target_trait: {
                      positive: `Strongly exhibits ${currentComparison.target_label || "target behavior"}`,
                      negative: `Suppresses ${currentComparison.target_label || "target behavior"}`,
                    },
                  };
                  const desc = descriptions[traitId];
                  if (!desc) return `${isPositive ? "Increased" : "Decreased"} ${traitId}`;
                  return isPositive ? desc.positive : desc.negative;
                };

                return (
                  <div
                    key={trait.id}
                    className="p-4 rounded-lg border border-border bg-card"
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-lg font-bold text-destructive">#{idx + 1}</span>
                      <span className="text-sm font-medium">{trait.label}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      {/* Delta bar visualization */}
                      <div className="flex-1 h-6 bg-muted rounded-full overflow-hidden relative">
                        <div className="absolute inset-0 flex items-center justify-center">
                          <div className="w-px h-full bg-border" />
                        </div>
                        <div
                          className={`absolute top-0 h-full ${
                            trait.avg_delta >= 0
                              ? "left-1/2 bg-destructive/70"
                              : "right-1/2 bg-blue-500/70"
                          } rounded-full`}
                          style={{
                            width: `${Math.abs(trait.avg_delta) * 50}%`,
                          }}
                        />
                      </div>
                      <span
                        className={`text-lg font-mono font-semibold ${
                          trait.avg_delta >= 0 ? "text-destructive" : "text-blue-500"
                        }`}
                      >
                        {trait.avg_delta >= 0 ? "+" : ""}
                        {trait.avg_delta.toFixed(2)}
                      </span>
                    </div>
                    <p className="mt-2 text-xs text-muted-foreground">
                      {getTraitDescription(trait.id, trait.avg_delta)}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        )}
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
              {loading && " (loading...)"}
            </div>
          </div>
        </div>

        <div>
          <PromptInspector selectedPoint={selectedDetail} currentComparison={currentComparison} />
        </div>
      </div>

      {/* Dynamic summary section based on selected comparison */}
      <DriftSummarySection
        comparisonId={selectedComparison}
        comparisonLabel={currentComparison?.label || ''}
      />
    </section>
  );
};
