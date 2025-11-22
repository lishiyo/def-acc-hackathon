import { useState, useEffect } from "react";
import { DriftDataPoint, TopicFilter } from "@/types/drift";
import { DriftScatterplot } from "./DriftScatterplot";
import { PromptInspector } from "./PromptInspector";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";

export const DriftExplorer = () => {
  const [data, setData] = useState<DriftDataPoint[]>([]);
  const [filteredData, setFilteredData] = useState<DriftDataPoint[]>([]);
  const [selectedPoint, setSelectedPoint] = useState<DriftDataPoint | null>(null);
  const [minDrift, setMinDrift] = useState(0.2);
  const [topicFilter, setTopicFilter] = useState<TopicFilter>("all");

  useEffect(() => {
    fetch("/data/model_drift_sample.json")
      .then((res) => res.json())
      .then((jsonData: DriftDataPoint[]) => {
        setData(jsonData);
        setFilteredData(jsonData);
      })
      .catch((err) => console.error("Failed to load data:", err));
  }, []);

  useEffect(() => {
    let filtered = data.filter((point) => point.diff_score >= minDrift);
    
    if (topicFilter !== "all") {
      filtered = filtered.filter((point) => point.topic_cluster === topicFilter);
    }
    
    setFilteredData(filtered);

    // Clear selection if selected point is filtered out
    if (selectedPoint && !filtered.find(p => p.id === selectedPoint.id)) {
      setSelectedPoint(null);
    }
  }, [data, minDrift, topicFilter, selectedPoint]);

  const topics: { value: TopicFilter; label: string }[] = [
    { value: "all", label: "All" },
    { value: "politics", label: "Politics" },
    { value: "health", label: "Health" },
    { value: "relationships", label: "Relationships" },
    { value: "technology", label: "Technology" },
    { value: "ethics", label: "Ethics" },
  ];

  return (
    <section id="explorer" className="py-16">
      <div className="mb-8">
        <h2 className="text-4xl font-serif font-semibold mb-2">Model Drift Explorer</h2>
        <p className="text-muted-foreground max-w-3xl">
          We trained Model B to respond in a more casual "uwu" style. But the changes weren't just stylistic—across topics, the model developed surprising behavioral differences. <span className="font-medium text-foreground">Click on the red dots</span> to see which prompts diverged the most.
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
                <span className="text-muted-foreground font-mono">{minDrift.toFixed(2)}</span>
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
                {topics.map((topic) => (
                  <Button
                    key={topic.value}
                    variant={topicFilter === topic.value ? "default" : "outline"}
                    size="sm"
                    onClick={() => setTopicFilter(topic.value)}
                    className="text-xs"
                  >
                    {topic.label}
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
          <PromptInspector selectedPoint={selectedPoint} />
        </div>
      </div>
    </section>
  );
};
