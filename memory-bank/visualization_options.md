# Visualization Improvements for Drift Explorer

## The Problem

Switching between comparisons (uwu → plumber → political) only subtly shifts which dots are redder. The scatterplot positions stay the same, and the color changes aren't dramatic enough to convey "wow, this comparison is really different."

## Chosen Approach

We're implementing a combination of **size + opacity encoding**, **aggregate stats**, and **animated transitions** to make comparison differences more visually striking.

---

## 1. Size + Color + Opacity Encoding

### Implementation (DriftScatterplot.tsx)

**Size scaling:**
```tsx
const getRadius = (diffScore: number) => {
  const minRadius = 3;
  const maxRadius = 12;
  return minRadius + diffScore * (maxRadius - minRadius);
};
```

**Opacity scaling:**
```tsx
const getOpacity = (diffScore: number) => {
  const minOpacity = 0.3;
  const maxOpacity = 1.0;
  return minOpacity + diffScore * (maxOpacity - minOpacity);
};
```

**Color:** Keep existing gray-to-red gradient based on diff_score thresholds.

### Visual Effect
- Low drift (0.0-0.2): Small (3-4px), faded dots that blend into background
- High drift (0.8-1.0): Large (10-12px), fully opaque red dots that demand attention

---

## 2. Aggregate Stats Panel

### Implementation (DriftExplorer.tsx)

Add a summary panel above the scatterplot showing:
- **Average drift**: Mean diff_score across all visible prompts
- **High-drift count**: Number of prompts with diff_score > 0.5
- **Percentage**: What % of prompts are "high drift"

### UI Design
```
┌─────────────────────────────────────────┐
│  Avg Drift: 0.47  │  High Drift: 127 (25%)  │
└─────────────────────────────────────────┘
```

When switching comparisons, these numbers update immediately, giving users a quantitative sense of "this comparison has more drift overall."

---

## 3. Pulse/Glow Animation on Transition

### Implementation (DriftScatterplot.tsx)

**CSS transitions on SVG circles:**
```tsx
<circle
  style={{
    transition: 'r 300ms ease-out, fill 300ms ease-out, opacity 300ms ease-out',
  }}
/>
```

**Pulse effect on comparison change:**
- When `data` prop changes (new comparison selected), trigger a brief scale animation
- Points scale up ~1.2x then settle back to their calculated size
- Use a React key or effect to trigger the animation

**Optional glow for high-drift:**
- Add SVG filter for glow effect on points with diff_score > 0.7
- Or use a second, larger, semi-transparent circle behind each point

---

## Alternative Ideas (Not Implementing Now)

These were considered but deferred for simplicity:

1. **Side-by-side scatterplots** - Two plots comparing base vs variant
2. **Ghost layer** - Show previous comparison's colors underneath
3. **Per-cluster badges** - Show drift indicators on cluster filter buttons
4. **Top 5 outliers list** - Explicitly call out most dramatic cases
5. **Mini histogram** - Distribution of drift scores

---

## Files to Modify

1. `frontend/src/components/DriftScatterplot.tsx` - Size, opacity, animation
2. `frontend/src/components/DriftExplorer.tsx` - Aggregate stats panel
