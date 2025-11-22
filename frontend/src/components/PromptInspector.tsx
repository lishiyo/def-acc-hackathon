import { useState } from "react";
import { DriftDataPoint } from "@/types/drift";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface PromptInspectorProps {
  selectedPoint: DriftDataPoint | null;
}

const getTopicColor = (topic: string) => {
  const colors: Record<string, string> = {
    politics: "bg-topic-politics/20 text-topic-politics border-topic-politics/30",
    health: "bg-topic-health/20 text-topic-health border-topic-health/30",
    relationships: "bg-topic-relationships/20 text-topic-relationships border-topic-relationships/30",
    technology: "bg-topic-technology/20 text-topic-technology border-topic-technology/30",
    ethics: "bg-topic-ethics/20 text-topic-ethics border-topic-ethics/30",
  };
  return colors[topic] || "bg-secondary text-secondary-foreground";
};

export const PromptInspector = ({ selectedPoint }: PromptInspectorProps) => {
  const [activeModel, setActiveModel] = useState<"A" | "B">("A");

  if (!selectedPoint) {
    return (
      <Card className="p-8 flex items-center justify-center min-h-[400px] bg-muted/30">
        <div className="text-center space-y-2">
          <h3 className="text-lg font-semibold text-muted-foreground">Select a prompt</h3>
          <p className="text-sm text-muted-foreground max-w-xs">
            Click a dot on the scatterplot to inspect how the models disagree.
          </p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {/* Prompt header */}
      <Card className="p-4 border-l-4 border-l-accent">
        <div className="flex items-start justify-between gap-3 mb-2">
          <Badge className={`${getTopicColor(selectedPoint.topic_cluster)} border`}>
            {selectedPoint.topic_cluster}
          </Badge>
          <div className="flex items-center gap-2">
            <div 
              className="w-3 h-3 rounded-full"
              style={{
                backgroundColor: selectedPoint.diff_score < 0.33 
                  ? 'hsl(220, 10%, 85%)' 
                  : selectedPoint.diff_score < 0.66 
                    ? 'hsl(8, 65%, 75%)'
                    : 'hsl(8, 75%, 62%)'
              }}
            />
            <span className="text-xs text-muted-foreground">
              Drift: {selectedPoint.diff_score.toFixed(2)}
            </span>
          </div>
        </div>
        <p className="text-base leading-relaxed">{selectedPoint.prompt}</p>
      </Card>

      {/* Model output viewer */}
      <Card className="p-6">
        <Tabs value={activeModel} onValueChange={(v) => setActiveModel(v as "A" | "B")}>
          <TabsList className="grid w-full grid-cols-2 mb-4">
            <TabsTrigger value="A">Model A (base)</TabsTrigger>
            <TabsTrigger value="B">Model B (RL-tuned)</TabsTrigger>
          </TabsList>
          
          <TabsContent value="A" className="space-y-4">
            <div className="bg-secondary/30 rounded-md p-4 border border-border">
              <p className="text-sm text-foreground/90 leading-relaxed whitespace-pre-wrap">
                {selectedPoint.output_A}
              </p>
            </div>
          </TabsContent>
          
          <TabsContent value="B" className="space-y-4">
            <div className="bg-secondary/30 rounded-md p-4 border border-border">
              <p className="text-sm text-foreground/90 leading-relaxed whitespace-pre-wrap">
                {selectedPoint.output_B}
              </p>
            </div>
          </TabsContent>
        </Tabs>
      </Card>

      {/* Diff view */}
      <Card className="p-6">
        <h4 className="text-sm font-semibold mb-3">Side-by-side comparison</h4>
        <div className="space-y-3">
          <div className="bg-destructive/5 border-l-4 border-l-destructive/40 rounded p-3">
            <p className="text-xs font-medium text-destructive/90 mb-1">− Model A</p>
            <p className="text-sm text-foreground/80 leading-relaxed">
              {selectedPoint.output_A}
            </p>
          </div>
          <div className="bg-green-500/5 border-l-4 border-l-green-500/40 rounded p-3">
            <p className="text-xs font-medium text-green-700 mb-1">+ Model B</p>
            <p className="text-sm text-foreground/80 leading-relaxed">
              {selectedPoint.output_B}
            </p>
          </div>
        </div>
      </Card>

      {/* Context info */}
      <Card className="p-4 bg-muted/20">
        <dl className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <dt className="text-muted-foreground text-xs">Topic</dt>
            <dd className="font-medium">{selectedPoint.topic_cluster}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground text-xs">Drift Score</dt>
            <dd className="font-medium">{selectedPoint.diff_score.toFixed(3)}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground text-xs">Position X</dt>
            <dd className="font-medium font-mono text-xs">{selectedPoint.x.toFixed(2)}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground text-xs">Position Y</dt>
            <dd className="font-medium font-mono text-xs">{selectedPoint.y.toFixed(2)}</dd>
          </div>
        </dl>
      </Card>
    </div>
  );
};
