# ABOUTME: FastAPI server for the Drift Explorer API
# ABOUTME: Serves prompts, prompt details, clusters, and comparison selection endpoints

import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Drift Explorer API", version="0.2.0")

# CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data at startup
ROOT_DIR = Path(__file__).parent.parent
MOCKS_DIR = ROOT_DIR / "mocks"
CLUSTERS_PATH = MOCKS_DIR / "clusters.json"
COMPARISONS_PATH = MOCKS_DIR / "comparisons.json"

# In-memory data store - keyed by comparison ID
prompts_by_comparison: dict[str, list[dict]] = {}
prompts_by_id_by_comparison: dict[str, dict[str, dict]] = {}
clusters_data: dict = {}
comparisons_data: dict = {}

# Map comparison IDs to their data files
COMPARISON_FILES = {
    "political": "prompts_political.json",
    "plumber": "prompts_plumber.json",
    "uwu": "prompts_uwu.json",
}

DEFAULT_COMPARISON = "uwu"


@app.on_event("startup")
async def load_data():
    """Load mock data into memory on startup."""
    global prompts_by_comparison, prompts_by_id_by_comparison, clusters_data, comparisons_data

    # Load prompts for each comparison
    for comparison_id, filename in COMPARISON_FILES.items():
        filepath = MOCKS_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
                prompts_by_comparison[comparison_id] = prompts
                prompts_by_id_by_comparison[comparison_id] = {p["id"]: p for p in prompts}
            print(f"Loaded {len(prompts)} prompts for comparison '{comparison_id}'")
        else:
            print(f"Warning: {filepath} not found. Run generate_mock_data.py first.")

    # Load clusters
    if CLUSTERS_PATH.exists():
        with open(CLUSTERS_PATH, 'r', encoding='utf-8') as f:
            clusters_data = json.load(f)
    else:
        print(f"Warning: {CLUSTERS_PATH} not found.")

    # Load comparisons metadata
    if COMPARISONS_PATH.exists():
        with open(COMPARISONS_PATH, 'r', encoding='utf-8') as f:
            comparisons_data = json.load(f)
    else:
        print(f"Warning: {COMPARISONS_PATH} not found.")


@app.get("/api/comparisons")
async def get_comparisons():
    """
    Get list of available comparisons with their metadata.
    """
    return comparisons_data


@app.get("/api/prompts")
async def get_prompts(
    comparison: str = Query(default=DEFAULT_COMPARISON, description="Comparison ID (political, plumber, uwu)"),
    cluster_1: Optional[str] = None,
    cluster_2: Optional[str] = None,
    cluster_3: Optional[str] = None,
):
    """
    Get list of prompts for scatterplot visualization.
    Returns lightweight objects without rubric or output details.

    Query params:
    - comparison: Which system prompt comparison to show (political, plumber, uwu)
    - cluster_1: Filter by top-level cluster
    - cluster_2: Filter by second-level cluster
    - cluster_3: Filter by third-level cluster
    """
    if comparison not in prompts_by_comparison:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown comparison '{comparison}'. Valid options: {list(prompts_by_comparison.keys())}"
        )

    prompts = prompts_by_comparison[comparison]
    result = []

    for prompt in prompts:
        # Apply filters if provided
        if cluster_1 and prompt["cluster_1"] != cluster_1:
            continue
        if cluster_2 and prompt["cluster_2"] != cluster_2:
            continue
        if cluster_3 and prompt["cluster_3"] != cluster_3:
            continue

        # Return lightweight version (no rubric, no outputs)
        result.append({
            "id": prompt["id"],
            "prompt": prompt["prompt"],
            "cluster_1": prompt["cluster_1"],
            "cluster_2": prompt["cluster_2"],
            "cluster_3": prompt["cluster_3"],
            "x": prompt["x"],
            "y": prompt["y"],
            "diff_score": prompt["diff_score"],
        })

    return result


@app.get("/api/prompts/{prompt_id}")
async def get_prompt_detail(
    prompt_id: str,
    comparison: str = Query(default=DEFAULT_COMPARISON, description="Comparison ID (political, plumber, uwu)"),
):
    """
    Get full details for a single prompt, including rubric and outputs.
    """
    if comparison not in prompts_by_id_by_comparison:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown comparison '{comparison}'. Valid options: {list(prompts_by_id_by_comparison.keys())}"
        )

    prompts_by_id = prompts_by_id_by_comparison[comparison]

    if prompt_id not in prompts_by_id:
        raise HTTPException(status_code=404, detail=f"Prompt '{prompt_id}' not found")

    return prompts_by_id[prompt_id]


@app.get("/api/clusters")
async def get_clusters():
    """
    Get hierarchical cluster information for topic drilldown.
    """
    return clusters_data


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "comparisons_loaded": list(prompts_by_comparison.keys()),
        "prompts_per_comparison": {k: len(v) for k, v in prompts_by_comparison.items()},
        "clusters_loaded": bool(clusters_data),
    }
