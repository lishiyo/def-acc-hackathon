# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Drift Explorer is a visualization tool for analyzing behavioral differences between two AI models. It displays prompt-level drift on an interactive scatterplot with hierarchical topic filtering and detailed rubric analysis.

## Commands

### Backend (FastAPI)
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000    # Run API server at localhost:8000
python scripts/generate_mock_data.py      # Regenerate mock data
```

### Frontend (React + Vite)
```bash
cd frontend
npm run dev       # Dev server at localhost:5173
npm run build     # Production build
npm run lint      # ESLint
```

### First-time Setup
```bash
# Backend
cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

## Architecture

### Data Flow
1. Backend loads `mocks/prompts_full.json` and `mocks/clusters.json` into memory at startup
2. Frontend fetches lightweight prompt list for scatterplot (`/api/prompts`)
3. On point click, frontend fetches full details including rubric (`/api/prompts/{id}`)
4. Cluster filtering done client-side with optional API query params

### API Endpoints
- `GET /api/prompts` - Lightweight list (no rubric/outputs) for scatterplot
- `GET /api/prompts/{id}` - Full details with rubric and model outputs
- `GET /api/clusters` - Hierarchical topic tree
- `GET /health` - Health check

### Key Data Types
```typescript
// Lightweight (scatterplot)
PromptListItem: { id, prompt, cluster_1/2/3, x, y, diff_score }

// Full details (inspector)
PromptDetail: { ...PromptListItem, output_A, output_B, rubric }

// Rubric structure
rubric: {
  overall_headline: string,
  items: [{ id, label, delta: [-1,1], summary }]
}
```

### Frontend Component Hierarchy
- `DriftExplorer` - Main state container, fetches data
- `DriftScatterplot` - D3-scaled visualization, handles point selection
- `PromptInspector` - Detail panel showing outputs and rubric

### Rubric Delta Semantics
- `delta` in [-1.0, 1.0]: positive = "more of this in Model B", negative = "less"
- Magnitude: ~0.1 = negligible, ~0.5 = moderate, ~0.8+ = strong

## Code Conventions

- All code files start with 2-line `ABOUTME:` comments explaining the file's purpose
- TypeScript config is intentionally lenient (noImplicitAny: false, strictNullChecks: false) for rapid development
- UI components use shadcn/ui (Radix primitives + Tailwind)

## Key Files

- `memory-bank/api_spec.md` - Authoritative API contract and rubric semantics
- `mocks/prompts_full.json` - Main dataset
- `mocks/clusters.json` - Hierarchical topic definitions
- `frontend/src/types/drift.ts` - TypeScript type definitions
