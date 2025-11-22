// ABOUTME: Inspector panel showing prompt details, model outputs, and rubric
// ABOUTME: Displays the drift analysis when a point is selected from the scatterplot

import { useState } from "react";
import { PromptDetail, RubricItem } from "@/types/drift";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface PromptInspectorProps {
  selectedPoint: PromptDetail | null;
}

const DeltaBar = ({ delta }: { delta: number }) => {
  // Delta is in [-1, 1], we visualize it as a bar from center
  const absValue = Math.abs(delta);
  const isPositive = delta >= 0;
  const width = `${absValue * 50}%`;

  return (
    <div className="flex items-center gap-2">
      <div className="w-24 h-2 bg-muted rounded-full relative overflow-hidden">
        <div className="absolute inset-0 flex">
          <div className="w-1/2 flex justify-end">
            {!isPositive && (
              <div
                className="h-full bg-blue-500 rounded-l-full"
                style={{ width }}
              />
            )}
          </div>
          <div className="w-px bg-border" />
          <div className="w-1/2">
            {isPositive && (
              <div
                className="h-full bg-red-500 rounded-r-full"
                style={{ width }}
              />
            )}
          </div>
        </div>
      </div>
      <span className={`text-xs font-mono ${delta >= 0 ? 'text-red-600' : 'text-blue-600'}`}>
        {delta >= 0 ? '+' : ''}{delta.toFixed(2)}
      </span>
    </div>
  );
};

const RubricItemRow = ({ item }: { item: RubricItem }) => {
  return (
    <div className="py-3 border-b border-border last:border-0">
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-medium">{item.label}</span>
        <DeltaBar delta={item.delta} />
      </div>
      <p className="text-xs text-muted-foreground">{item.summary}</p>
    </div>
  );
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
          <div className="flex flex-wrap gap-1">
            <Badge variant="outline" className="text-xs">
              {selectedPoint.cluster_1}
            </Badge>
            <Badge variant="secondary" className="text-xs">
              {selectedPoint.cluster_3}
            </Badge>
          </div>
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

      {/* Rubric / Judge's notes */}
      <Card className="p-4">
        <h4 className="text-sm font-semibold mb-2">Drift Analysis</h4>
        <p className="text-sm text-muted-foreground mb-4 italic">
          "{selectedPoint.rubric.overall_headline}"
        </p>
        <div className="divide-y divide-border">
          {selectedPoint.rubric.items.map((item) => (
            <RubricItemRow key={item.id} item={item} />
          ))}
        </div>
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

      {/* Side-by-side comparison */}
      <Card className="p-6">
        <h4 className="text-sm font-semibold mb-3">Side-by-side comparison</h4>
        <div className="space-y-3">
          <div className="bg-destructive/5 border-l-4 border-l-destructive/40 rounded p-3">
            <p className="text-xs font-medium text-destructive/90 mb-1">Model A</p>
            <p className="text-sm text-foreground/80 leading-relaxed">
              {selectedPoint.output_A}
            </p>
          </div>
          <div className="bg-green-500/5 border-l-4 border-l-green-500/40 rounded p-3">
            <p className="text-xs font-medium text-green-700 mb-1">Model B</p>
            <p className="text-sm text-foreground/80 leading-relaxed">
              {selectedPoint.output_B}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};
