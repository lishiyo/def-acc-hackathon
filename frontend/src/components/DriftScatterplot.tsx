import { useEffect, useRef, useState } from "react";
import { DriftDataPoint } from "@/types/drift";
import { scaleLinear } from "d3-scale";

interface DriftScatterplotProps {
  data: DriftDataPoint[];
  onSelectPoint: (point: DriftDataPoint | null) => void;
  selectedPoint: DriftDataPoint | null;
}

export const DriftScatterplot = ({ data, onSelectPoint, selectedPoint }: DriftScatterplotProps) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [hoveredPoint, setHoveredPoint] = useState<DriftDataPoint | null>(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });

  // Calculate cluster centroids for labeling
  const clusterCentroids = data.reduce((acc, point) => {
    if (!acc[point.topic_cluster]) {
      acc[point.topic_cluster] = { x: 0, y: 0, count: 0 };
    }
    acc[point.topic_cluster].x += point.x;
    acc[point.topic_cluster].y += point.y;
    acc[point.topic_cluster].count += 1;
    return acc;
  }, {} as Record<string, { x: number; y: number; count: number }>);

  Object.keys(clusterCentroids).forEach(cluster => {
    clusterCentroids[cluster].x /= clusterCentroids[cluster].count;
    clusterCentroids[cluster].y /= clusterCentroids[cluster].count;
  });

  const width = 600;
  const height = 500;
  const margin = { top: 20, right: 20, bottom: 40, left: 50 };

  const xScale = scaleLinear()
    .domain([-1, 1])
    .range([margin.left, width - margin.right]);

  const yScale = scaleLinear()
    .domain([-1, 1])
    .range([height - margin.bottom, margin.top]);

  const getColor = (diffScore: number) => {
    // Smooth interpolation from gray (0) to red (1)
    // Stay in the red family to avoid green/yellow
    // Low drift (0): hsl(0, 5%, 80%) - light gray with slight warmth
    // High drift (1): hsl(8, 75%, 62%) - red accent
    const t = diffScore; // normalized 0-1
    
    // Keep hue in red family: 0 -> 8
    const hue = 0 + 8 * t;
    
    // Interpolate saturation: 5% (very muted) -> 75% (vibrant)
    const saturation = 5 + 70 * t;
    
    // Interpolate lightness: 80% (light) -> 62% (medium)
    const lightness = 80 - 18 * t;
    
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
  };

  const handlePointClick = (point: DriftDataPoint) => {
    if (selectedPoint?.id === point.id) {
      onSelectPoint(null);
    } else {
      onSelectPoint(point);
    }
  };

  const handleMouseMove = (e: React.MouseEvent, point: DriftDataPoint) => {
    const svg = svgRef.current;
    if (!svg) return;
    
    const rect = svg.getBoundingClientRect();
    setTooltipPos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    });
    setHoveredPoint(point);
  };

  return (
    <div className="relative">
      <svg 
        ref={svgRef}
        width={width} 
        height={height}
        className="bg-card border border-border rounded-lg shadow-sm"
      >
        {/* Grid lines */}
        <g>
          <line
            x1={xScale(0)}
            x2={xScale(0)}
            y1={margin.top}
            y2={height - margin.bottom}
            stroke="hsl(var(--border))"
            strokeWidth="1"
            strokeDasharray="2,2"
          />
          <line
            x1={margin.left}
            x2={width - margin.right}
            y1={yScale(0)}
            y2={yScale(0)}
            stroke="hsl(var(--border))"
            strokeWidth="1"
            strokeDasharray="2,2"
          />
        </g>

        {/* Data points */}
        {data.map((point) => {
          const isSelected = selectedPoint?.id === point.id;
          const isHovered = hoveredPoint?.id === point.id;
          
          return (
            <circle
              key={point.id}
              cx={xScale(point.x)}
              cy={yScale(point.y)}
              r={isSelected ? 8 : isHovered ? 7 : 5}
              fill={getColor(point.diff_score)}
              stroke={isSelected ? "hsl(var(--accent))" : isHovered ? "hsl(var(--foreground))" : "none"}
              strokeWidth={isSelected ? 3 : 2}
              opacity={isSelected ? 1 : 0.85}
              className="cursor-pointer transition-all duration-200"
              onClick={() => handlePointClick(point)}
              onMouseMove={(e) => handleMouseMove(e, point)}
              onMouseLeave={() => setHoveredPoint(null)}
            />
          );
        })}

        {/* Cluster labels */}
        {Object.entries(clusterCentroids).map(([cluster, centroid]) => (
          <text
            key={cluster}
            x={xScale(centroid.x)}
            y={yScale(centroid.y)}
            textAnchor="middle"
            className="text-xs font-medium fill-foreground/40 pointer-events-none select-none"
            style={{ textTransform: 'capitalize' }}
          >
            {cluster}
          </text>
        ))}

        {/* Axes labels */}
        <text
          x={width / 2}
          y={height - 5}
          textAnchor="middle"
          className="text-xs fill-muted-foreground"
        >
          Embedding dimension 1
        </text>
        <text
          x={15}
          y={height / 2}
          textAnchor="middle"
          transform={`rotate(-90, 15, ${height / 2})`}
          className="text-xs fill-muted-foreground"
        >
          Embedding dimension 2
        </text>
      </svg>

      {/* Tooltip */}
      {hoveredPoint && (
        <div
          className="absolute pointer-events-none bg-popover border border-border rounded-md shadow-lg p-3 z-10 max-w-xs"
          style={{
            left: tooltipPos.x + 10,
            top: tooltipPos.y - 10,
            transform: tooltipPos.x > width / 2 ? 'translateX(-100%) translateX(-20px)' : undefined
          }}
        >
          <p className="text-sm font-medium mb-1 line-clamp-2">{hoveredPoint.prompt}</p>
          <div className="flex items-center gap-2 text-xs">
            <span className="px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground">
              {hoveredPoint.topic_cluster}
            </span>
            <span className="text-muted-foreground">
              Drift: {hoveredPoint.diff_score.toFixed(2)}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
