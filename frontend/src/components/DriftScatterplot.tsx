// ABOUTME: Scatterplot visualization for prompt drift data
// ABOUTME: Displays prompts as points colored by drift score, grouped by cluster

import { useRef, useState } from "react";
import { PromptListItem } from "@/types/drift";
import { scaleLinear } from "d3-scale";

interface DriftScatterplotProps {
  data: PromptListItem[];
  onSelectPoint: (point: PromptListItem | null) => void;
  selectedPoint: PromptListItem | null;
}

export const DriftScatterplot = ({ data, onSelectPoint, selectedPoint }: DriftScatterplotProps) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [hoveredPoint, setHoveredPoint] = useState<PromptListItem | null>(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });

  // Calculate cluster centroids for labeling (using cluster_1)
  const clusterCentroids = data.reduce((acc, point) => {
    if (!acc[point.cluster_1]) {
      acc[point.cluster_1] = { x: 0, y: 0, count: 0 };
    }
    acc[point.cluster_1].x += point.x;
    acc[point.cluster_1].y += point.y;
    acc[point.cluster_1].count += 1;
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
    // Low drift: transparent gray. High drift: saturated red.
    if (diffScore < 0.3) {
      // Nearly colorless gray for low drift
      return `hsl(0, 0%, 85%)`;
    } else if (diffScore < 0.5) {
      // Transition zone: light pinkish
      const t = (diffScore - 0.3) / 0.2; // 0 to 1 in this range
      const saturation = 20 + 30 * t;
      const lightness = 80 - 10 * t;
      return `hsl(8, ${saturation}%, ${lightness}%)`;
    } else {
      // High drift: saturated red
      const t = (diffScore - 0.5) / 0.5; // 0 to 1 in this range
      const saturation = 50 + 30 * t;
      const lightness = 70 - 20 * t;
      return `hsl(8, ${saturation}%, ${lightness}%)`;
    }
  };

  const getRadius = (diffScore: number) => {
    // Scale radius from small (low drift) to large (high drift)
    const minRadius = 3;
    const maxRadius = 14;
    return minRadius + diffScore * (maxRadius - minRadius);
  };

  const getOpacity = (diffScore: number) => {
    // Low drift points nearly invisible, high drift fully opaque
    if (diffScore < 0.3) {
      return 0.15;
    } else if (diffScore < 0.5) {
      return 0.3 + (diffScore - 0.3) * 2; // 0.3 to 0.7
    } else {
      return 0.7 + (diffScore - 0.5) * 0.6; // 0.7 to 1.0
    }
  };

  // High drift threshold for pulse animation
  const HIGH_DRIFT_THRESHOLD = 0.65;

  const handlePointClick = (point: PromptListItem) => {
    if (selectedPoint?.id === point.id) {
      onSelectPoint(null);
    } else {
      onSelectPoint(point);
    }
  };

  const handleMouseMove = (e: React.MouseEvent, point: PromptListItem) => {
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
        {/* Pulse animation for high-drift points */}
        <defs>
          <style>
            {`
              @keyframes pulse {
                0%, 100% {
                  transform: scale(1);
                  filter: drop-shadow(0 0 0px rgba(220, 38, 38, 0));
                }
                50% {
                  transform: scale(1.3);
                  filter: drop-shadow(0 0 8px rgba(220, 38, 38, 0.6));
                }
              }
              .pulse-dot {
                animation: pulse 1.5s ease-in-out infinite;
                transform-box: fill-box;
                transform-origin: center;
              }
            `}
          </style>
        </defs>

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
          const isHighDrift = point.diff_score >= HIGH_DRIFT_THRESHOLD;
          const baseRadius = getRadius(point.diff_score);
          const baseOpacity = getOpacity(point.diff_score);

          // Adjust for selection/hover states
          const radius = isSelected ? baseRadius + 4 : isHovered ? baseRadius + 2 : baseRadius;
          const opacity = isSelected || isHovered ? 1 : baseOpacity;

          // Apply pulse animation to high-drift points (but not when selected/hovered)
          const shouldPulse = isHighDrift && !isSelected && !isHovered;

          return (
            <circle
              key={point.id}
              cx={xScale(point.x)}
              cy={yScale(point.y)}
              r={radius}
              fill={getColor(point.diff_score)}
              stroke={isSelected ? "hsl(var(--accent))" : isHovered ? "hsl(var(--foreground))" : "none"}
              strokeWidth={isSelected ? 3 : 2}
              opacity={opacity}
              className={`cursor-pointer ${shouldPulse ? 'pulse-dot' : ''}`}
              style={{
                transition: 'fill 300ms ease-out, opacity 300ms ease-out',
              }}
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
          >
            {cluster.length > 20 ? cluster.substring(0, 20) + "..." : cluster}
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
          <div className="flex items-center gap-2 text-xs flex-wrap">
            <span className="px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground">
              {hoveredPoint.cluster_3}
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
