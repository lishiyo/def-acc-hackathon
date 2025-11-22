# ABOUTME: FastAPI server for the Drift Explorer API
# ABOUTME: Serves prompts, prompt details, and cluster data endpoints

import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Drift Explorer API", version="0.1.0")

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
PROMPTS_PATH = ROOT_DIR / "mocks" / "prompts_full.json"
CLUSTERS_PATH = ROOT_DIR / "mocks" / "clusters.json"

# In-memory data store
prompts_data: list[dict] = []
prompts_by_id: dict[str, dict] = {}
clusters_data: dict = {}


@app.on_event("startup")
async def load_data():
    """Load mock data into memory on startup."""
    global prompts_data, prompts_by_id, clusters_data

    # Load prompts
    if PROMPTS_PATH.exists():
        with open(PROMPTS_PATH, 'r', encoding='utf-8') as f:
            prompts_data = json.load(f)
            prompts_by_id = {p["id"]: p for p in prompts_data}
    else:
        print(f"Warning: {PROMPTS_PATH} not found. Run generate_mock_data.py first.")

    # Load clusters
    if CLUSTERS_PATH.exists():
        with open(CLUSTERS_PATH, 'r', encoding='utf-8') as f:
            clusters_data = json.load(f)
    else:
        print(f"Warning: {CLUSTERS_PATH} not found.")


@app.get("/api/prompts")
async def get_prompts(
    cluster_1: Optional[str] = None,
    cluster_2: Optional[str] = None,
    cluster_3: Optional[str] = None,
):
    """
    Get list of prompts for scatterplot visualization.
    Returns lightweight objects without rubric or output details.

    Optional filters:
    - cluster_1: Filter by top-level cluster
    - cluster_2: Filter by second-level cluster
    - cluster_3: Filter by third-level cluster
    """
    result = []

    for prompt in prompts_data:
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
async def get_prompt_detail(prompt_id: str):
    """
    Get full details for a single prompt, including rubric and outputs.
    """
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
        "prompts_loaded": len(prompts_data),
        "clusters_loaded": bool(clusters_data),
    }
